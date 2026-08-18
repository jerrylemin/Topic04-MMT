import ast
from pathlib import Path

from flask import Flask, Response, current_app, jsonify, make_response, render_template, request, session
from jinja2 import TemplateNotFound
from werkzeug.exceptions import HTTPException

from audit_service import list_logs, log_event, log_login_attempt, log_query_event
from auth_service import authenticate_secure, authenticate_vulnerable, create_login_session, logout_user
from config import Config, QUOTE_INPUT, SEARCH_EXPANDED_INPUT
from database import close_db, init_db, query_all, query_one
from error_service import categorize_database_error, error_inspector
from secure_queries import secure_search, secure_user_detail
from seed import reset_database
from trace_service import build_trace, clear_traces, get_trace, new_trace_id, save_trace
from validation import ValidationError, input_signals, positive_int, validate_keyword, validate_password, validate_username
from vulnerable_queries import vulnerable_search, vulnerable_user_detail


CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
    "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'; connect-src 'self'"
)


def _render(template: str, status: int = 200, **context):
    context.setdefault("mode", "informational")
    context.setdefault("feature", "overview")
    context.setdefault("trace", None)
    context.setdefault("result", None)
    context.setdefault("results", [])
    context.setdefault("error_info", None)
    context.setdefault("audit_logs", [])
    context.setdefault("security_controls", [])
    context.setdefault("code_comparison", [])
    try:
        return render_template(template, **context), status
    except TemplateNotFound:
        # ponytail: keeps backend routes runnable while UI templates remain an independent slice.
        return Response(f"Lab05: {template}", status=status, mimetype="text/plain")


def _source_snippet(filename: str, function_name: str) -> dict:
    path = Path(__file__).with_name(filename)
    source = path.read_text(encoding="utf-8")
    node = next(
        (item for item in ast.walk(ast.parse(source))
         if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == function_name),
        None,
    )
    if node is None:
        return {"file": filename, "function": function_name, "line_start": 0, "line_end": 0, "code": ""}
    lines = source.splitlines()
    return {
        "file": filename, "function": function_name,
        "line_start": node.lineno, "line_end": node.end_lineno,
        "code": "\n".join(lines[node.lineno - 1:node.end_lineno]),
    }


def _code_comparisons() -> dict[str, dict]:
    def pair(vulnerable: dict, secure: dict, vulnerable_explanation: str, secure_explanation: str) -> dict:
        return {
            "vulnerable_file": vulnerable["file"], "vulnerable_function": vulnerable["function"],
            "vulnerable_lines": f'{vulnerable["line_start"]}-{vulnerable["line_end"]}',
            "vulnerable_code": vulnerable["code"], "vulnerable_explanation": vulnerable_explanation,
            "secure_file": secure["file"], "secure_function": secure["function"],
            "secure_lines": f'{secure["line_start"]}-{secure["line_end"]}',
            "secure_code": secure["code"], "secure_explanation": secure_explanation,
        }
    login_vulnerable = _source_snippet("vulnerable_queries.py", "vulnerable_login")
    login_secure = _source_snippet("auth_service.py", "authenticate_secure")
    search_vulnerable = _source_snippet("vulnerable_queries.py", "vulnerable_search")
    search_secure = _source_snippet("secure_queries.py", "secure_search")
    error = _source_snippet("error_service.py", "error_inspector")
    return {
        "login": pair(login_vulnerable, login_secure,
                      "Username được nối vào SQL và legacy digest cố tình yếu.",
                      "Username được bind; password được kiểm tra bằng check_password_hash."),
        "search": pair(search_vulnerable, search_secure,
                       "Keyword được nối trực tiếp vào LIKE.",
                       "LIKE dùng placeholder và tuple parameter."),
        "error": pair(error, error,
                      "Nhánh vulnerable chỉ hiển thị chẩn đoán local đã rút gọn.",
                      "Nhánh secure chỉ trả thông báo chung và error ID."),
    }


def _security_controls() -> list[dict]:
    def control(name, status, source, file, routes, risk, limitation):
        return {"name": name, "status": status, "source": source, "file": file,
                "routes": routes, "risk": risk, "limitation": limitation}
    return [
        control("Prepared statement", True, "sqlite3 placeholders", "secure_queries.py", "Secure routes", "SQL structure changes", "Only protects queries that use it"),
        control("Parameterized query", True, "Runtime query metadata", "secure_queries.py", "Secure routes", "SQL injection", "Does not replace authorization"),
        control("PBKDF2 password hashing", True, "Werkzeug", "seed.py", "Secure login", "Offline password attacks", "Demo work factor must be reviewed over time"),
        control("Unique salt", True, "Werkzeug-generated salt", "seed.py", "All demo users", "Precomputed hashes", "Hash is still sensitive"),
        control("Generic login error", True, "Single rejected decision", "app.py", "Secure login", "Username enumeration", "Timing controls are outside this local lab"),
        control("Generic database error", True, "Safe error inspector", "error_service.py", "Secure routes", "Internal disclosure", "Internal logs still need access control"),
        control("Input validation", True, "Trust-boundary validators", "validation.py", "All demo inputs", "Malformed input", "Does not replace prepared statements"),
        control("Result limit", 50, "SQL LIMIT", "secure_queries.py", "Secure search", "Large result sets", "Not pagination"),
        control("Session rotation", True, "session.clear before login", "auth_service.py", "Login", "Session fixation", "Signed client session model"),
        control("HttpOnly", current_app.config["SESSION_COOKIE_HTTPONLY"], "Flask config", "config.py", "Session cookie", "Script cookie access", "Does not stop CSRF"),
        control("SameSite", current_app.config["SESSION_COOKIE_SAMESITE"], "Flask config", "config.py", "Session cookie", "Cross-site requests", "Defense in depth"),
        control("Secure cookie", current_app.config["SESSION_COOKIE_SECURE"], "Environment config", "config.py", "Session cookie", "Cleartext transport", "False for fixed local HTTP"),
        control("CSP", True, "Response header", "app.py", "All routes", "Injection impact", "Defense in depth"),
        control("Request size limit", current_app.config["MAX_CONTENT_LENGTH"], "Flask config", "config.py", "All routes", "Oversized bodies", "Not rate limiting"),
        control("Least privilege simulation", True, "Fixed local SELECT flows", "database.py", "Vulnerable demos", "Database modification", "SQLite has no database-user permission model"),
        control("Logging", True, "Structured SQLite audit", "audit_service.py", "Security flows", "Missing accountability", "Local retention only"),
        control("WAF", False, "Not installed", "N/A", "None", "Known request patterns", "WAF never replaces fixing code"),
    ]


def _enrich_query_error(info: dict | None, query: dict, feature: str) -> dict | None:
    if info is None:
        return None
    return {
        **info,
        "query_template": query.get("query_template"),
        "input_insertion": "username_input" if feature == "login" else "keyword_inside_like_pattern",
        "root_cause": "Untrusted input was concatenated into SQL text.",
        "data_modified": False,
    }


def _flow_response(template: str, *, mode: str, feature: str, raw_input: str,
                   normalized_input: str, outcome: dict, error_info: dict | None,
                   action: str | list[str], username: str | None = None, expected_count: int | None = None,
                   status: int = 200):
    rows = outcome["rows"]
    trace_id = new_trace_id()
    session_created = bool(outcome.get("user"))
    trace = build_trace(
        mode=mode, feature=feature, raw_input=raw_input, normalized_input=normalized_input,
        query=outcome["query"], rows=rows, error_info=error_info, decision=outcome["decision"],
        expected_count=expected_count, session_created=session_created, trace_id=trace_id,
    )
    if feature == "login":
        trace["decision_inspector"].update({
            "username_submitted": username,
            "password_length": outcome.get("password_length", 0),
            "password_fingerprint": "[NOT STORED]",
            "user_matched": bool(outcome.get("user")),
            "password_verification_executed": outcome.get("password_verification_executed", mode == "vulnerable"),
            "password_verification_result": outcome.get("password_verification_result"),
        })
    comparisons = _code_comparisons()
    trace["code_comparison"] = comparisons.get(feature, comparisons["error"])
    error_category = (error_info or {}).get("category")
    log_query_event(mode=mode, feature=feature, query=outcome["query"], result_count=len(rows),
                    error_category=error_category, trace_id=trace_id)
    for event_action in ([action] if isinstance(action, str) else action):
        log_event(
            action=event_action, mode=mode, username_submitted=username,
            input_summary={"signals": input_signals(raw_input), "feature": feature},
            query=outcome["query"], decision=outcome["decision"], reason=outcome["reason"],
            result_count=len(rows), error_category=error_category, trace_id=trace_id,
        )
    if feature == "login":
        user = outcome.get("user")
        log_login_attempt(mode=mode, username=username or "", success=bool(user),
                          user_id=user["id"] if user else None, reason=outcome["reason"], trace_id=trace_id)
    trace["audit_inspector"] = {
        "action": action,
        "route": request.path,
        "mode": mode,
        "input_summary": {"signals": input_signals(raw_input), "feature": feature},
        "query_construction": outcome["query"].get("construction_method"),
        "decision": outcome["decision"],
        "reason": outcome["reason"],
        "result_count": len(rows),
        "error_category": error_category,
        "trace_id": trace_id,
    }
    trace["final_verdict"]["audit_event"] = action
    save_trace(trace)
    public_rows = [
        {key: value for key, value in dict(row).items()
         if key not in {"password_hash", "legacy_password_digest", "email"}}
        for row in rows
    ]
    response = make_response(_render(
        template, status, mode=mode, feature=feature, trace=trace,
        result=(public_rows[0] if public_rows else None), results=public_rows,
        error_info=error_info, security_controls=_security_controls(),
        code_comparison=comparisons.get(feature, comparisons["error"]), comparisons=comparisons,
    ))
    response.headers["X-Lab-Trace-ID"] = trace_id
    response.headers["X-Lab-Decision"] = outcome["decision"]
    response.headers["X-Lab-Result-Count"] = str(len(rows))
    response.headers["X-Lab-Error-Category"] = error_category or "none"
    response.headers["X-Lab-Prepared"] = str(bool(outcome["query"].get("prepared"))).lower()
    return response


def _validation_response(message: str):
    raw_input = (request.form.get("username") or request.args.get("keyword") or
                 request.args.get("id") or "")
    query = {
        "feature": "validation", "mode": "secure", "query_template": "[QUERY NOT EXECUTED]",
        "construction_method": "none", "final_query_masked": "[QUERY NOT EXECUTED]",
        "placeholder_count": 0, "parameters_masked": [], "prepared": False,
        "duration_ms": 0.0, "error": None,
    }
    outcome = {"rows": [], "query": query, "decision": "validation_failed", "reason": message}
    trace_id = new_trace_id()
    trace = build_trace(mode="secure", feature="validation", raw_input=raw_input,
                        normalized_input=raw_input, query=query, rows=[], error_info=None,
                        decision="validation_failed", trace_id=trace_id)
    save_trace(trace)
    log_event(action="validation_failed", mode="secure", username_submitted=None,
              input_summary={"signals": input_signals(raw_input)}, query=query,
              decision=outcome["decision"], reason=message, result_count=0,
              error_category="validation_error", trace_id=trace_id)
    response = make_response(_render("error.html", 400, mode="secure", feature="validation", error_info={
        "category": "validation_error", "handled": True, "user_message": message,
    }, trace=trace))
    response.headers["X-Lab-Trace-ID"] = trace_id
    response.headers["X-Lab-Decision"] = "validation_failed"
    response.headers["X-Lab-Error-Category"] = "validation_error"
    return response


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    app.teardown_appcontext(close_db)

    @app.after_request
    def security_headers(response):
        response.headers["Content-Security-Policy"] = CSP
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if "/login" in request.path or request.path == "/logout":
            response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/")
    def index():
        return _render("index.html", test_inputs=current_app.config["TEST_INPUTS"])

    @app.get("/dashboard")
    def dashboard():
        return _render("dashboard.html", audit_logs=[dict(row) for row in list_logs(20)])

    @app.post("/reset-lab")
    def reset_lab():
        reset_database()
        trace_id = new_trace_id()
        query = {"query_template": "fixed seed reset", "placeholder_count": 0}
        log_event(action="lab_reset", mode="maintenance", username_submitted=None,
                  input_summary={"source": "fixed route"}, query=query, decision="completed",
                  reason="local_demo_database_reseeded", result_count=0, error_category=None, trace_id=trace_id)
        return jsonify({"reset": True, "trace_id": trace_id})

    @app.route("/vulnerable/login", methods=["GET", "POST"])
    def vulnerable_login_route():
        if request.method == "GET":
            return _render("vulnerable/login.html", mode="vulnerable", feature="login",
                           test_inputs=current_app.config["TEST_INPUTS"])
        try:
            username = validate_username(request.form.get("username"), vulnerable=True)
            password = validate_password(request.form.get("password"))
        except ValidationError as exc:
            return _validation_response(str(exc))
        outcome = authenticate_vulnerable(username, password)
        error_info = error_inspector(outcome["query"]["error"], secure=False) if outcome["query"].get("error") else None
        error_info = _enrich_query_error(error_info, outcome["query"], "login")
        if outcome["user"]:
            create_login_session(outcome["user"], via="vulnerable_local_demo")
        if username == QUOTE_INPUT:
            action = ["login_quote_detected", "login_query_error", "database_error_handled"]
        elif outcome["decision"] == "local_demo_bypass":
            action = ["login_logic_changed", "login_bypass_local_demo"]
        else:
            action = "login_normal_success" if outcome["user"] else "login_normal_failed"
        return _flow_response("vulnerable/login_result.html", mode="vulnerable", feature="login",
                              raw_input=username, normalized_input=username, outcome=outcome,
                              error_info=error_info, action=action, username=username)

    @app.route("/secure/login", methods=["GET", "POST"])
    def secure_login_route():
        if request.method == "GET":
            return _render("secure/login.html", mode="secure", feature="login",
                           test_inputs=current_app.config["TEST_INPUTS"])
        try:
            username = validate_username(request.form.get("username"), vulnerable=False)
            password = validate_password(request.form.get("password"))
        except ValidationError as exc:
            return _validation_response(str(exc))
        outcome = authenticate_secure(username, password)
        if outcome["user"]:
            create_login_session(outcome["user"], via="secure_pbkdf2")
        action = "secure_login_success" if outcome["user"] else "secure_login_rejected"
        return _flow_response("secure/login_result.html", mode="secure", feature="login",
                              raw_input=username, normalized_input=username, outcome=outcome,
                              error_info=None, action=action, username=username)

    @app.post("/logout")
    def logout():
        logout_user()
        return jsonify({"logged_out": True})

    @app.get("/vulnerable/search")
    def vulnerable_search_route():
        submitted = "keyword" in request.args
        if not submitted:
            return _render("vulnerable/search.html", mode="vulnerable", feature="search",
                           test_inputs=current_app.config["TEST_INPUTS"])
        try:
            keyword = validate_keyword(request.args.get("keyword"), vulnerable=True)
        except ValidationError as exc:
            return _validation_response(str(exc))
        rows, query = vulnerable_search(keyword)
        error_info = error_inspector(query["error"], secure=False) if query.get("error") else None
        error_info = _enrich_query_error(error_info, query, "search")
        expected_rows, _ = secure_search(keyword)
        decision = "query_error" if error_info else ("unexpected_results" if len(rows) > len(expected_rows) else "expected_results")
        action = (["search_quote_detected", "search_query_error", "database_error_handled"] if keyword == QUOTE_INPUT else
                  ["search_condition_changed", "search_unexpected_result"] if keyword == SEARCH_EXPANDED_INPUT else "search_normal")
        outcome = {"rows": rows, "query": query, "decision": decision,
                   "reason": "sqlite_rejected_final_sql" if error_info else "result_set_compared_with_expected_filter"}
        return _flow_response("vulnerable/search_result.html", mode="vulnerable", feature="search",
                              raw_input=keyword, normalized_input=keyword, outcome=outcome,
                              error_info=error_info, action=action, expected_count=len(expected_rows))

    @app.get("/secure/search")
    def secure_search_route():
        submitted = "keyword" in request.args
        if not submitted:
            return _render("secure/search.html", mode="secure", feature="search",
                           test_inputs=current_app.config["TEST_INPUTS"])
        try:
            keyword = validate_keyword(request.args.get("keyword"), vulnerable=False)
        except ValidationError as exc:
            return _validation_response(str(exc))
        rows, query = secure_search(keyword)
        outcome = {"rows": rows, "query": query, "decision": "expected_results",
                   "reason": "parameter_binding_preserved_query_structure"}
        return _flow_response("secure/search_result.html", mode="secure", feature="search",
                              raw_input=keyword, normalized_input=keyword, outcome=outcome,
                              error_info=None, action="secure_search_completed", expected_count=len(rows))

    @app.get("/vulnerable/user")
    def vulnerable_user_route():
        try:
            user_id = positive_int(request.args.get("id"))
        except ValidationError as exc:
            return _validation_response(str(exc))
        rows, query = vulnerable_user_detail(user_id)
        outcome = {"rows": rows, "query": query, "decision": "found" if rows else "not_found", "reason": "fixed_numeric_demo"}
        return _flow_response("vulnerable/user_detail.html", mode="vulnerable", feature="user_detail",
                              raw_input=str(user_id), normalized_input=str(user_id), outcome=outcome,
                              error_info=None, action="user_detail_requested", status=200 if rows else 404)

    @app.get("/secure/user")
    def secure_user_route():
        try:
            user_id = positive_int(request.args.get("id"))
        except ValidationError as exc:
            return _validation_response(str(exc))
        rows, query = secure_user_detail(user_id)
        outcome = {"rows": rows, "query": query, "decision": "found" if rows else "not_found", "reason": "integer_validated_and_bound"}
        return _flow_response("secure/user_detail.html", mode="secure", feature="user_detail",
                              raw_input=str(user_id), normalized_input=str(user_id), outcome=outcome,
                              error_info=None, action="user_detail_requested", status=200 if rows else 404)

    @app.get("/comparison")
    def comparison():
        comparisons = _code_comparisons()
        return _render("comparison.html", code_comparison=comparisons["login"], comparisons=comparisons)

    @app.get("/security-controls")
    def security_controls():
        return _render("security_controls.html", security_controls=_security_controls())

    @app.get("/audit-logs")
    def audit_logs():
        return _render("audit_logs.html", audit_logs=[dict(row) for row in list_logs()])

    @app.get("/api/trace/<trace_id>")
    def trace_api(trace_id):
        trace = get_trace(trace_id)
        return jsonify(trace) if trace else (jsonify({"error": "trace not found"}), 404)

    @app.route("/api/trace/clear", methods=["GET", "POST"])
    def trace_clear():
        if request.method == "GET":
            return jsonify({"error": "method not allowed"}), 405
        clear_traces()
        return jsonify({"cleared": True})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "Lab05 SQL Injection Local Lab"})

    @app.errorhandler(404)
    def not_found(_error):
        return _render("error.html", 404, error_info={"category": "not_found", "user_message": "Không tìm thấy trang."})

    @app.errorhandler(413)
    def too_large(_error):
        return _render("error.html", 413, error_info={"category": "request_too_large", "user_message": "Request body vượt giới hạn."})

    @app.errorhandler(Exception)
    def safe_error(error):
        if isinstance(error, HTTPException):
            return error
        if current_app.config.get("TESTING"):
            raise error
        info = error_inspector(error, secure=True)
        return _render("error.html", 500, mode="secure", feature="error", error_info=info)

    with app.app_context():
        init_db()
        if query_one("SELECT id FROM users LIMIT 1") is None:
            reset_database()
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5005, debug=False)
