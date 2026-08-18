from flask import Flask, render_template


SCENARIOS = {
    "vulnerable_email_attack.html": {
        "title": "CSRF đổi email - vulnerable",
        "target": "http://127.0.0.1:5004/vulnerable/change-email",
        "method": "POST",
        "fields": {"email": "demo_changed@lab.local"},
        "expected": "Request có thể đổi email nếu cookie được gửi; attacker vẫn không đọc được response.",
    },
    "secure_email_attack.html": {
        "title": "Secure route - thiếu token",
        "target": "http://127.0.0.1:5004/secure/change-email",
        "method": "POST",
        "fields": {"email": "secure_attack@lab.local"},
        "expected": "Server từ chối vì Origin không hợp lệ hoặc thiếu CSRF token; email không đổi.",
    },
    "bad_token_attack.html": {
        "title": "Secure route - token không hợp lệ",
        "target": "http://127.0.0.1:5004/secure/change-email",
        "method": "POST",
        "fields": {"email": "bad_token@lab.local", "csrf_token": "fake_token_for_local_lab"},
        "expected": "Server trả 403; token giả không khớp token gắn với session.",
    },
}


def create_app(test_config=None):
    app = Flask(
        __name__, template_folder="attacker_templates", static_folder="static/attacker"
    )
    app.config.update(MAX_CONTENT_LENGTH=32 * 1024)
    if test_config:
        app.config.update(test_config)

    @app.after_request
    def local_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; "
            "form-action 'self' http://127.0.0.1:5004; connect-src 'self'; "
            "base-uri 'none'; object-src 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    @app.get("/")
    def index():
        return render_template("index.html")

    routes = {
        "/attack/vulnerable-email": "vulnerable_email_attack.html",
        "/attack/secure-email": "secure_email_attack.html",
        "/attack/bad-token": "bad_token_attack.html",
    }
    for route, template in routes.items():
        app.add_url_rule(
            route,
            endpoint=f"attack_{template}",
            view_func=lambda name=template: render_template(name, **SCENARIOS[name]),
        )

    @app.get("/origin-demo")
    def origin_demo():
        return render_template("origin_demo.html")

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "demo-page", "bind": "127.0.0.1:9004"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9004, debug=False)
