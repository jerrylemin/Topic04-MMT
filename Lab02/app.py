from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, g, jsonify, make_response, render_template, request

from config import Config, ROOT
from native_runner import run_native
from security_utils import is_local_host, is_local_origin, utf8_length, validate_name
from trace_models import build_trace
from trace_service import TraceService


PAGE_ROUTES = {
    "/": "index.html",
    "/vulnerable": "vulnerable.html",
    "/secure/length": "secure_length.html",
    "/secure/snprintf": "secure_snprintf.html",
    "/hardening": "hardening.html",
    "/gdb-guide": "gdb_guide.html",
    "/comparison": "comparison.html",
}
SOURCE_FILES = (
    "vulnerable_processor.c",
    "secure_length_processor.c",
    "secure_snprintf_processor.c",
)


def _sources() -> dict[str, str]:
    sources = {}
    for filename in SOURCE_FILES:
        path = ROOT / "native" / filename
        sources[filename] = path.read_text(encoding="utf-8") if path.is_file() else ""
    return sources


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    traces = TraceService(Path(app.config["TRACE_DIR"]))
    app.extensions["trace_service"] = traces
    build_info = {
        mode: {
            "binary": info["binary"],
            "profile": info["profile"],
            "compiler_flags": info["flags"],
            "verification": "pending local binary inspection",
        }
        for mode, info in app.config["MODES"].items()
    }
    sources = _sources()

    def wants_json() -> bool:
        return request.path.startswith("/api/") or request.accept_mimetypes.best == "application/json"

    def page(template: str, status: int = 200, **values):
        context = {"trace": None, "build_info": build_info, "sources": sources, "error": None}
        context.update(values)
        return render_template(template, **context), status

    def problem(message: str, status: int, template: str = "error.html"):
        if wants_json():
            return jsonify(error=message, status=status), status
        return page(template, status, error=message)

    @app.before_request
    def enforce_local_request():
        if not is_local_host(request.host, app.config["LOCAL_HOSTS"], app.config["PORT"]):
            return jsonify(error="Host không được phép."), 400
        if request.method == "POST" and not is_local_origin(
            request.headers.get("Origin"), app.config["LOCAL_HOSTS"], app.config["PORT"]
        ):
            return jsonify(error="Origin không được phép."), 403
        return None

    @app.after_request
    def add_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        if getattr(g, "lab_mode", None):
            response.headers["X-Lab-Mode"] = g.lab_mode
        return response

    @app.errorhandler(413)
    def request_too_large(_error):
        return problem("Request body vượt giới hạn 4096 byte.", 413)

    @app.errorhandler(404)
    def not_found(_error):
        return problem("Không tìm thấy tài nguyên.", 404)

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return problem("Phương thức HTTP không được phép.", 405)

    @app.errorhandler(500)
    def internal_error(_error):
        return problem("Lỗi nội bộ đã được chuẩn hóa; xem log local để chẩn đoán.", 500)

    for route, template in PAGE_ROUTES.items():
        endpoint = "page_" + (route.strip("/").replace("/", "_") or "home")
        app.add_url_rule(route, endpoint, lambda template=template: page(template))

    @app.get("/health")
    def health():
        return jsonify(status="ok", service="lab02")

    def submit(template: str, path: str, forced_mode: str | None = None):
        if request.mimetype not in {
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        }:
            return problem("Content-Type phải là form data.", 415, template)
        try:
            name = validate_name(request.form.get("name"), app.config["MAX_NAME_BYTES"])
        except ValueError as exc:
            return problem(str(exc), 400, template)

        mode = forced_mode or request.form.get("mode", "vulnerable_asan")
        allowed = (
            {"vulnerable_asan", "vulnerable_debug", "secure_hardened"}
            if forced_mode is None
            else {forced_mode}
        )
        if mode not in allowed or mode not in app.config["MODES"]:
            return problem("Mode không được phép.", 400, template)
        if mode == "vulnerable_debug" and utf8_length(name) > 31:
            return problem(
                "Input dài phải dùng vulnerable_asan trên web; vulnerable_debug chỉ dành cho GDB local.",
                400,
                template,
            )
        g.lab_mode = mode
        started = datetime.now(timezone.utc).isoformat()
        summary = {
            "method": request.method,
            "url": request.base_url,
            "path": path,
            "content_type": request.mimetype,
            "content_length": request.content_length,
            "form_field": "name",
            "name_length_chars": len(name),
            "name_length_bytes": utf8_length(name),
            "mode": mode,
            "timestamp": started,
        }
        native_result = run_native(
            mode,
            name,
            modes=app.config["MODES"],
            root=ROOT,
            timeout=app.config["SUBPROCESS_TIMEOUT"],
            max_name_bytes=app.config["MAX_NAME_BYTES"],
        )
        trace = build_trace(
            traces.new_id(),
            mode,
            name,
            summary,
            native_result,
            app.config["MODES"][mode],
        )
        traces.save(trace)
        if mode == "secure_hardened":
            template = "hardening.html"
        status = 504 if native_result["status"] == "timeout" else 503 if native_result["status"] == "unavailable" else 200
        if wants_json():
            response = make_response(jsonify(trace=trace, native_result=native_result), status)
        else:
            response = make_response(page(template, status, trace=trace)[0], status)
        response.headers["X-Trace-ID"] = trace["trace_id"]
        return response

    @app.post("/submit")
    def submit_vulnerable():
        return submit("vulnerable.html", "/submit")

    @app.post("/secure/length/submit")
    def submit_secure_length():
        return submit("secure_length.html", "/secure/length/submit", "secure_length")

    @app.post("/secure/snprintf/submit")
    def submit_secure_snprintf():
        return submit("secure_snprintf.html", "/secure/snprintf/submit", "secure_snprintf")

    @app.get("/api/trace/<trace_id>")
    def get_trace(trace_id: str):
        trace = traces.get(trace_id)
        return jsonify(trace) if trace else (jsonify(error="Trace không tồn tại."), 404)

    @app.post("/api/trace/clear")
    def clear_traces():
        return jsonify(cleared=traces.clear())

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=False, use_reloader=False)
