from pathlib import Path

import bleach
from flask import Flask, Response, make_response, render_template, request, session
from markupsafe import Markup

from config import Config
from database import close_db, get_db, init_db
from trace_service import reflected_trace, simple_trace, stored_trace

PRODUCTS = ["Bàn phím cơ", "Chuột không dây", "Màn hình 27 inch", "Laptop học tập"]
ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "code"]
CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    app.teardown_appcontext(close_db)

    def traced(template: str, trace: dict, **context) -> Response:
        """Render twice so Response Inspector reports the actual generated HTML."""
        body = render_template(template, trace=trace, **context)
        trace["response_summary"].update({
            "headers": {"Content-Security-Policy": CSP if trace["mode"] == "secure" else "(không áp dụng)",
                        "X-Lab-Mode": trace["mode"]},
            "html_snippet": body[max(0, body.find("result") - 80):body.find("result") + 320],
            "length": len(body.encode("utf-8")),
        })
        body = render_template(template, trace=trace, **context)
        trace["completed_at"] = trace["steps"][-1]["timestamp"] if trace["steps"] else trace["started_at"]
        return make_response(body)

    @app.after_request
    def headers(response: Response) -> Response:
        secure = request.path.startswith("/secure") or request.path in {"/profile", "/security-headers"}
        response.headers["X-Lab-Mode"] = "secure" if secure else "vulnerable" if request.path.startswith("/vulnerable") else "information"
        if secure:
            response.headers.update({"Content-Security-Policy": CSP, "X-Content-Type-Options": "nosniff",
                                     "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY",
                                     "Permissions-Policy": "camera=(), microphone=(), geolocation=()"})
        return response

    @app.route("/")
    def index():
        return render_template("index.html")

    def search(secure: bool = False):
        raw = request.args.get("q", "")
        error = "Từ khóa tối đa 200 ký tự." if len(raw) > 200 else ""
        q = raw[:200]
        results = [product for product in PRODUCTS if q.lower() in product.lower()] if q and not error else []
        mode = "secure" if secure else "vulnerable"
        trace = reflected_trace(request, q, mode, results, error)
        trace["response_summary"]["before_escape"] = q
        trace["response_summary"]["after_escape"] = str(Markup.escape(q)) if secure else q
        return traced(f"reflected_{mode}.html", trace, q=q if secure else Markup(q), results=results, error=error)

    app.add_url_rule("/vulnerable/search", "vulnerable_search", lambda: search(False))
    app.add_url_rule("/secure/search", "secure_search", lambda: search(True))

    def comments(secure: bool = False):
        db, error, inserted = get_db(), "", False
        body = request.form.get("body", "").strip()
        if request.method == "POST":
            if request.form.get("action") == "clear":
                db.execute("DELETE FROM comments")
                db.commit()
            else:
                author = request.form.get("author", "").strip()
                if not author or not body:
                    error = "Tên và nội dung bình luận không được để trống."
                elif len(author) > 60 or len(body) > 2000:
                    error = "Tên tối đa 60 và bình luận tối đa 2000 ký tự."
                else:
                    db.execute("INSERT INTO comments(post_id,author,body) VALUES(1,?,?)", (author, body))
                    db.commit()
                    inserted = True
        rows = [dict(row) for row in db.execute("SELECT * FROM comments WHERE post_id=? ORDER BY id", (1,))]
        mode = "secure" if secure else "vulnerable"
        trace = stored_trace(request, mode, rows, body, inserted, error)
        for row in rows:
            if secure:
                row["sanitized"] = Markup(bleach.clean(row["body"], tags=ALLOWED_TAGS, attributes={}, protocols=[], strip=True))
            else:
                row["body"] = Markup(row["body"])
        return traced(f"stored_{mode}.html", trace, comments=rows, error=error)

    app.add_url_rule("/vulnerable/post/1/comments", "vulnerable_comments", lambda: comments(False), methods=["GET", "POST"])
    app.add_url_rule("/secure/post/1/comments", "secure_comments", lambda: comments(True), methods=["GET", "POST"])

    def dom(secure: bool = False):
        mode = "secure" if secure else "vulnerable"
        return traced(f"dom_{mode}.html", simple_trace(request, "dom", mode))

    app.add_url_rule("/vulnerable/dom-search", "vulnerable_dom", lambda: dom(False))
    app.add_url_rule("/secure/dom-search", "secure_dom", lambda: dom(True))

    @app.route("/profile")
    def profile():
        session["display_name"] = "Sinh viên Lab Local"
        return traced("profile.html", simple_trace(request, "profile"), cookie_secure=app.config["SESSION_COOKIE_SECURE"])

    @app.route("/security-headers")
    def security_headers():
        return traced("security_headers.html", simple_trace(request, "headers"), csp=CSP)

    @app.route("/test-results")
    def test_results():
        log = Path(app.root_path, "evidence/logs/pytest.txt")
        data = log.read_bytes() if log.exists() else b"Chua chay pytest."
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = data.decode("utf-16")
        return render_template("test_results.html", log=text)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", message="Không tìm thấy trang."), 404

    with app.app_context():
        init_db()
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
