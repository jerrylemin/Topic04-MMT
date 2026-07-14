from types import SimpleNamespace

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

from audit_service import list_logs
from auth import authenticate, login_required, login_user, logout_user
from config import Config
from database import close_db, init_db, query_one
from seed import reset_database
from services import (CODE_COMPARISONS, add_to_cart, cart_for_user, get_product, get_user,
                      list_products, secure_checkout, secure_invoice, secure_profile,
                      update_cart, vulnerable_checkout, vulnerable_invoice, vulnerable_profile)
from trace_service import clear_traces, get_trace
from validators import ValidationError, integer


CSP = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"


def _invoice_view(invoice):
    return SimpleNamespace(**invoice) if invoice else None


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    app.teardown_appcontext(close_db)

    @app.after_request
    def security_headers(response):
        response.headers.update({
            "Content-Security-Policy": CSP,
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Cache-Control": "no-store",
        })
        return response

    @app.route("/")
    def index():
        return render_template("index.html", current_user=get_user(session["user_id"]) if session.get("user_id") else None)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = ""
        if request.method == "POST":
            user = authenticate(request.form.get("username", ""), request.form.get("password", ""))
            if user:
                login_user(user)
                return redirect(url_for("products"))
            error = "Sai tên đăng nhập hoặc mật khẩu lab."
        return render_template("login.html", error=error), 401 if error else 200

    @app.post("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.get("/products")
    @login_required
    def products():
        return render_template("products.html", products=list_products(), current_user=get_user(session["user_id"]))

    @app.get("/products/<int:product_id>")
    @login_required
    def product_detail(product_id):
        product = get_product(product_id)
        if not product:
            abort(404)
        return render_template("products.html", products=[product], product=product, current_user=get_user(session["user_id"]))

    @app.get("/cart")
    @login_required
    def cart():
        items = cart_for_user(session["user_id"])
        return render_template("cart.html", cart_items=items, total=sum(item["line_total"] for item in items),
                               current_user=get_user(session["user_id"]))

    @app.post("/cart/add")
    @login_required
    def cart_add():
        try:
            add_to_cart(session["user_id"], request.form.get("product_id"), request.form.get("quantity", 1))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        return redirect(url_for("cart"))

    @app.post("/cart/update")
    @login_required
    def cart_update():
        try:
            update_cart(session["user_id"], request.form.get("product_id"), request.form.get("quantity"))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        return redirect(url_for("cart"))

    def checkout_page(mode: str):
        items = cart_for_user(session["user_id"])
        product = get_product(integer(request.values.get("product_id", items[0]["product_id"] if items else 5), "product_id"))
        return render_template(f"{mode}/checkout.html", product=product, cart_items=items, mode=mode,
                               current_user=get_user(session["user_id"]))

    @app.route("/vulnerable/checkout", methods=["GET", "POST"])
    @login_required
    def checkout_vulnerable():
        if request.method == "GET":
            return checkout_page("vulnerable")
        try:
            invoice, trace = vulnerable_checkout(session["user_id"], request.form.get("product_id"),
                                                  request.form.get("quantity"), request.form.get("price"))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        return render_template("vulnerable/checkout_result.html", invoice=invoice, trace=trace, mode="vulnerable")

    @app.route("/secure/checkout", methods=["GET", "POST"])
    @login_required
    def checkout_secure():
        if request.method == "GET":
            return checkout_page("secure")
        try:
            invoice, trace = secure_checkout(session["user_id"], request.form.get("product_id"),
                                              request.form.get("quantity"), request.form.get("price"))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        return render_template("secure/checkout_result.html", invoice=invoice, trace=trace, mode="secure")

    @app.get("/vulnerable/invoice")
    @login_required
    def invoice_vulnerable():
        try:
            invoice, trace = vulnerable_invoice(session["user_id"], request.args.get("id"))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        if not invoice:
            return render_template("error.html", message="Không tìm thấy invoice."), 404
        return render_template("vulnerable/invoice.html", invoice=_invoice_view(invoice), trace=trace, mode="vulnerable")

    @app.get("/secure/invoice")
    @login_required
    def invoice_secure():
        try:
            invoice, trace, status = secure_invoice(session["user_id"], session["role"], request.args.get("id"))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        if status == 403:
            return render_template("error.html", status_code=403, message="Bạn không có quyền xem invoice này.", trace=trace), 403
        if status == 404:
            return render_template("error.html", status_code=404, message="Không tìm thấy invoice.", trace=trace), 404
        return render_template("secure/invoice.html", invoice=_invoice_view(invoice), trace=trace,
                               authorization=trace["authorization_inspector"],
                               current_user=get_user(session["user_id"]), mode="secure")

    @app.get("/vulnerable/profile")
    @login_required
    def profile_vulnerable():
        return render_template("vulnerable/profile.html", user=get_user(session["user_id"]), mode="vulnerable")

    @app.post("/vulnerable/profile/update")
    @login_required
    def profile_vulnerable_update():
        try:
            user, trace = vulnerable_profile(session["user_id"], request.form.get("user_id"),
                                              request.form.get("email", ""), request.form.get("role", ""))
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        return render_template("vulnerable/profile_result.html", user=user, trace=trace, mode="vulnerable")

    @app.get("/secure/profile")
    @login_required
    def profile_secure():
        return render_template("secure/profile.html", user=get_user(session["user_id"]), mode="secure")

    @app.post("/secure/profile/update")
    @login_required
    def profile_secure_update():
        try:
            user, trace = secure_profile(session["user_id"], request.form)
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        return render_template("secure/profile_result.html", user=user, trace=trace, mode="secure")

    @app.get("/comparison")
    def comparison():
        return render_template("comparison.html", comparisons=CODE_COMPARISONS)

    @app.get("/security-controls")
    def security_controls():
        def control(name, enabled, file, route, risk, limit):
            return {"name": name, "enabled": enabled, "file": file, "route": route, "risk": risk, "limit": limit}

        controls = [
            control("Server-side price lookup", True, "services.py", "/secure/checkout", "Client price tampering", "Không thay quantity validation"),
            control("Session-based identity", True, "auth.py", "secure routes", "Forged user_id", "Session vẫn cần secret mạnh"),
            control("Object-level authorization", True, "authorization.py", "/secure/invoice", "IDOR", "Phải áp dụng trên từng object"),
            control("Field allowlist", True, "services.py", "/secure/profile/update", "Mass assignment", "Admin cần route riêng"),
            control("Input type validation", True, "validators.py", "practice routes", "Sai kiểu dữ liệu", "Không thay authorization"),
            control("Range validation", True, "validators.py", "/secure/checkout", "Quantity bất thường", "Còn phải kiểm tra stock"),
            control("Parameterized SQL", True, "database.py", "database routes", "SQL Injection", "Không tự vá business logic"),
            control("Database transaction", True, "services.py", "/secure/checkout", "Invoice ghi dở dang", "SQLite chỉ phù hợp lab local"),
            control("Audit logging", True, "audit_service.py", "practice routes", "Thiếu dấu vết tampering", "Không trực tiếp chặn request"),
            control("HttpOnly", True, "config.py", "session cookie", "JavaScript đọc cookie", "Không thay authorization"),
            control("SameSite=Lax", True, "config.py", "session cookie", "Một phần request cross-site", "Không phải bản vá Parameter Tampering"),
            control("Secure cookie", app.config["SESSION_COOKIE_SECURE"], "config.py", "HTTPS deployment", "Cookie qua HTTP", "Tắt có chủ đích trên local HTTP"),
            control("Request size limit", True, "config.py", "all routes", "Body quá lớn", "Không validate nội dung"),
            control("CSRF protection", False, "not configured", "state-changing forms", "Cross-site requests", "Lớp khác, không vá IDOR/tampering"),
        ]
        return render_template("security_controls.html", controls=controls)

    @app.get("/audit-logs")
    @login_required
    def audit_logs():
        user_id = request.args.get("user_id")
        try:
            user_id = integer(user_id, "user_id") if user_id else None
        except ValidationError as exc:
            return render_template("error.html", message=str(exc)), 400
        logs = list_logs(user_id, request.args.get("action", ""), request.args.get("mode", ""),
                         request.args.get("decision", ""), request.args.get("trace_id", ""))
        return render_template("audit_logs.html", logs=logs)

    @app.get("/api/trace/<trace_id>")
    @login_required
    def trace_api(trace_id):
        trace = get_trace(trace_id)
        return jsonify(trace) if trace else (jsonify({"error": "trace not found"}), 404)

    @app.post("/api/trace/clear")
    @login_required
    def trace_clear():
        clear_traces()
        return jsonify({"cleared": True})

    @app.post("/reset-lab")
    @login_required
    def reset_lab():
        reset_database()
        logout_user()
        return redirect(url_for("login"))

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "Lab03 Parameter Tampering"})

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", message="Không tìm thấy trang."), 404

    @app.errorhandler(413)
    def too_large(_error):
        return render_template("error.html", message="Request body vượt giới hạn 64 KiB."), 413

    with app.app_context():
        init_db()
        if query_one("SELECT id FROM users LIMIT 1") is None:
            reset_database()
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5003, debug=False)
