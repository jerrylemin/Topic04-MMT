import ast
from pathlib import Path

from flask import Flask, Response, current_app, g, jsonify, redirect, render_template, request, session, url_for
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash

from audit_service import list_logs, log_event
from auth import (authenticate, is_recently_reauthenticated, login_required, login_user,
                  logout_user, reauthenticate)
from config import Config
from csrf_service import mask_csrf_token, rotate_csrf_token, validate_session_csrf
from database import close_db, get_db, init_db, query_all, query_one, transaction
from origin_service import validate_origin_or_referer
from security_utils import ValidationError, fingerprint, mask_secret, positive_int, validate_email, validate_new_password
from seed import reset_database
from trace_models import TraceStep
from trace_service import clear_traces, get_trace, request_trace, save_trace


VICTIM_ORIGINS = {"http://127.0.0.1:5004", "http://localhost:5004"}
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
       "object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'; connect-src 'self'")


def _render(template: str, status: int = 200, **context):
    cookie_name = current_app.config["SESSION_COOKIE_NAME"]
    cookie_value = request.cookies.get(cookie_name)
    try:
        submitted_token = request.form.get("csrf_token")
    except Exception:
        submitted_token = None
    context.setdefault("cookie_inspector", {
        "name": cookie_name,
        "present": bool(cookie_value),
        "httponly": current_app.config["SESSION_COOKIE_HTTPONLY"],
        "samesite": current_app.config["SESSION_COOKIE_SAMESITE"],
        "secure": current_app.config["SESSION_COOKIE_SECURE"],
        "path": current_app.config.get("SESSION_COOKIE_PATH") or "/",
        "host": request.host,
        "scheme": request.scheme,
        "masked_value": mask_secret(cookie_value),
    })
    context.setdefault("token_inspector", {
        "session_present": bool(session.get("csrf_token")),
        "form_present": bool(submitted_token),
        "expected_masked": mask_csrf_token(session.get("csrf_token")),
        "submitted_masked": mask_csrf_token(submitted_token),
        "comparison_method": "hmac.compare_digest",
        "validation_status": context.get("trace", {}).get("csrf_token_status", "issued") if isinstance(context.get("trace"), dict) else "issued",
        "rotation_status": "rotated" if isinstance(context.get("trace"), dict) and context["trace"].get("csrf_token_status") == "rotated" else "not_rotated",
        "issued_time": session.get("csrf_token_issued_at"),
    })
    trace = context.get("trace")
    if isinstance(trace, dict) and trace.get("trace_id"):
        row = query_one("SELECT * FROM state_history WHERE trace_id = ? ORDER BY id DESC LIMIT 1", (trace["trace_id"],))
        context.setdefault("state_record", dict(row) if row else None)
    context.setdefault("code_snippets", _source_snippets())
    try:
        return render_template(template, **context), status
    except TemplateNotFound:
        # ponytail: core routes stay testable while the independently-owned template slice lands.
        return Response(f"Lab04 template: {template}", status=status, mimetype="text/plain")


def _source_snippet(filename: str, function_name: str) -> dict:
    path = Path(__file__).with_name(filename)
    source = path.read_text(encoding="utf-8")
    node = next(
        (item for item in ast.walk(ast.parse(source)) if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == function_name),
        None,
    )
    if node is None:
        return {"file": filename, "function": function_name, "line_start": 0, "line_end": 0, "code": ""}
    lines = source.splitlines()
    return {
        "file": filename,
        "function": function_name,
        "line_start": node.lineno,
        "line_end": node.end_lineno,
        "code": "\n".join(lines[node.lineno - 1:node.end_lineno]),
    }


def _source_snippets() -> list[dict]:
    return [
        _source_snippet("victim_app.py", "vulnerable_change_email"),
        _source_snippet("victim_app.py", "secure_change_email"),
        _source_snippet("csrf_service.py", "validate_csrf_token"),
        _source_snippet("origin_service.py", "validate_origin_or_referer"),
        _source_snippet("victim_app.py", "logout"),
        _source_snippet("victim_app.py", "reset_lab"),
    ]


def _user(user_id=None):
    row = query_one("SELECT * FROM users WHERE id = ?", (user_id or session.get("user_id"),))
    return dict(row) if row else None


def _available_email(value: str | None, user_id: int) -> str:
    email = validate_email(value)
    if query_one("SELECT id FROM users WHERE email = ? AND id <> ?", (email, user_id)):
        raise ValidationError("Email đã được dùng bởi tài khoản demo khác.")
    return email


def _record_state(user_id: int, field: str, old, new, route: str, mode: str, trace_id: str, db=None) -> None:
    connection = db or get_db()
    connection.execute(
        """INSERT INTO state_history
           (user_id, field_name, old_value, new_value, source_route, mode, trace_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, field, str(old), str(new), route, mode, trace_id),
    )


def _detailed_steps(action: str, mode: str, decision: str, reason: str, csrf_status: str,
                    origin_status: str, before: dict, after: dict, status: int,
                    reauth_status: str) -> list[TraceStep]:
    origin = request.headers.get("Origin")
    attacker_request = bool(origin and origin not in VICTIM_ORIGINS)
    state_changed = before != after and bool(after)
    origin_checked = origin_status != "not_checked"
    csrf_checked = csrf_status != "not_required"
    reauth_checked = reauth_status != "not_required"
    rows = [
        ("Victim Browser", "Browser prepares request",
         f"The browser prepared {request.method} {request.path}.", "observed"),
        ("Attacker Page", "Form source classified",
         "Origin is external to the victim application." if attacker_request else "No attacker origin was observed for this request.",
         "observed" if attacker_request else "not_applicable"),
        ("Cookie Policy", "Session cookie inclusion observed",
         "The victim session cookie was present on the actual request." if request.cookies.get("lab04_session") else "No victim session cookie was present.",
         "observed"),
        ("HTTP Request", "Request headers received",
         f"Origin={origin or 'missing'}; Referer={request.headers.get('Referer') or 'missing'}.", "observed"),
        ("Flask Router", "Route matched", f"Flask selected the handler for {request.path}.", "observed"),
        ("Authentication", "Signed session checked",
         f"Session user={session.get('username') or 'anonymous'}.", "allowed" if session.get("user_id") else "denied"),
        ("Origin Validation", "Origin/Referer policy",
         f"Validation result: {origin_status}." if origin_checked else "This vulnerable or non-secure flow does not enforce Origin/Referer.",
         "allowed" if origin_status in {"origin_allowed", "referer_allowed"} else ("denied" if origin_checked else "not_applicable")),
        ("CSRF Validation", "Synchronizer token policy",
         f"Server-side token status: {csrf_status}." if csrf_checked else "This flow does not require a CSRF token.",
         "allowed" if csrf_status in {"valid", "rotated"} else ("denied" if csrf_checked else "not_applicable")),
        ("Re-authentication", "Recent authentication policy",
         f"Re-authentication status: {reauth_status}." if reauth_checked else "Re-authentication is not required for this action.",
         "allowed" if reauth_status == "success" else ("denied" if reauth_checked else "not_applicable")),
        ("Input Validation", "Bounded input validation",
         "Input passed the route-specific validation before mutation." if decision == "allowed" else "Mutation did not proceed after a security check denied the request.",
         "allowed" if decision == "allowed" else "not_reached"),
        ("Business Logic", "Action decision", f"Decision={decision}; reason={reason}.", decision),
        ("SQLite", "Database state",
         "A parameterized transaction changed the recorded state." if state_changed else "No state change was committed.",
         "changed" if state_changed else "unchanged"),
        ("Audit Logging", "Security event recorded", f"Audit event {action} is linked to this trace.", "recorded"),
        ("HTTP Response", "Response produced", f"Victim response status is {status}.", "observed"),
        ("Same-Origin Policy", "Attacker response readability",
         "The cross-origin request may be sent, but attacker script cannot read the victim response." if attacker_request else "No cross-origin attacker response read was attempted.",
         "blocked" if attacker_request else "not_applicable"),
        ("Final Result", "Security verdict", f"{decision}: {reason}.", decision),
    ]
    return [TraceStep(index, layer, title, description, status=step_status,
                      technique=f"{layer} observation and policy decision",
                      input_data={"method": request.method, "path": request.path, "step": index},
                      output_data={"decision": decision, "http_status": status, "step_status": step_status},
                      code_reference={"file": "victim_app.py", "function": action, "line": "runtime"},
                      security_meaning="Observed request data and server-side decision; no secret values are stored.")
            for index, (layer, title, description, step_status) in enumerate(rows, 1)]


def _audit_and_trace(action: str, mode: str, decision: str, reason: str, *,
                     csrf_status="not_required", origin_status="not_checked",
                     before=None, after=None, status=200, reauth_status="not_required",
                     trace_id=None) -> dict:
    trace = request_trace(
        mode, action, csrf_status=csrf_status, origin_decision=origin_status,
        state_before=before, state_after=after, status=status, result=decision,
        reauth_status=reauth_status,
        steps=_detailed_steps(action, mode, decision, reason, csrf_status, origin_status,
                              before or {}, after or {}, status, reauth_status),
        trace_id=trace_id,
    )
    log_event(action, mode=mode, decision=decision, reason=reason, csrf_status=csrf_status,
              state_before=before, state_after=after, trace_id=trace["trace_id"])
    saved = save_trace(trace)
    g.trace_saved = True
    return saved


def _secure_checks(action: str, state_before: dict):
    origin = validate_origin_or_referer(request.headers.get("Origin"), request.headers.get("Referer"))
    if not origin.allowed:
        event = origin.reason
        trace = _audit_and_trace(event, "secure", "denied", origin.reason, before=state_before,
                                 status=403, origin_status=origin.reason)
        return origin, "not_checked", _render("secure/csrf_error.html", 403, reason=origin.reason, trace=trace)
    csrf_result = validate_session_csrf(request.form.get("csrf_token"))
    csrf_status = csrf_result["status"]
    if csrf_status != "valid":
        event = "csrf_token_missing" if csrf_status == "missing" else "csrf_token_invalid"
        trace = _audit_and_trace(event, "secure", "denied", event, csrf_status=csrf_status,
                                 origin_status=origin.reason, before=state_before, status=403)
        return origin, csrf_status, _render("secure/csrf_error.html", 403, reason=event, trace=trace)
    return origin, csrf_status, None


def _protected_route_checks(denied_action: str, state_before: dict):
    origin = validate_origin_or_referer(
        request.headers.get("Origin"), request.headers.get("Referer")
    )
    csrf_result = validate_session_csrf(request.form.get("csrf_token"))
    csrf_status = csrf_result["status"]
    if not origin.allowed or csrf_status != "valid":
        reason = origin.reason if not origin.allowed else f"csrf_token_{csrf_status}"
        trace = _audit_and_trace(
            denied_action,
            "secure",
            "denied",
            reason,
            csrf_status=csrf_status,
            origin_status=origin.reason,
            before=state_before,
            status=403,
        )
        return _render(
            "secure/csrf_error.html", 403, reason=reason, trace=trace
        )
    return None


def _do_transfer(sender_id: int, receiver_id: int, amount: int, trace_id: str) -> dict:
    with transaction() as db:
        sender = db.execute("SELECT demo_balance FROM users WHERE id = ?", (sender_id,)).fetchone()
        receiver = db.execute("SELECT demo_balance FROM users WHERE id = ?", (receiver_id,)).fetchone()
        if not sender or not receiver:
            raise ValidationError("Tài khoản nhận không tồn tại.")
        if sender_id == receiver_id:
            raise ValidationError("Không thể chuyển cho chính mình.")
        if sender["demo_balance"] < amount:
            raise ValidationError("Số dư không đủ.")
        before = {"sender_balance": sender["demo_balance"], "receiver_balance": receiver["demo_balance"]}
        db.execute("UPDATE users SET demo_balance = demo_balance - ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
                   (amount, sender_id))
        db.execute("UPDATE users SET demo_balance = demo_balance + ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
                   (amount, receiver_id))
        cursor = db.execute(
            "INSERT INTO demo_transfers (sender_id, receiver_id, amount, status, trace_id) VALUES (?, ?, ?, 'completed', ?)",
            (sender_id, receiver_id, amount, trace_id),
        )
        after = {"sender_balance": sender["demo_balance"] - amount,
                 "receiver_balance": receiver["demo_balance"] + amount,
                 "transaction_id": cursor.lastrowid}
        _record_state(sender_id, "demo_balance", before["sender_balance"], after["sender_balance"],
                      request.path, "secure" if request.path.startswith("/secure") else "vulnerable", trace_id, db)
    return {"before": before, "after": after}


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, template_folder="victim_templates", static_folder="static")
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
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        })
        if request.path.startswith(("/secure/", "/login", "/profile")):
            response.headers["Cache-Control"] = "no-store"
        if not getattr(g, "trace_saved", False):
            _audit_and_trace("request_observed", "informational", "observed", "route_completed",
                             status=response.status_code)
        return response

    @app.get("/")
    def index():
        return _render("index.html", current_user=_user() if session.get("user_id") else None)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return _render("login.html", demo_username="victim", demo_password="Victim123!")
        user = authenticate(request.form.get("username", ""), request.form.get("password", ""))
        if not user:
            _audit_and_trace("login_failed", "authentication", "denied", "invalid_credentials", status=401)
            return _render("login.html", 401, error="Sai tên đăng nhập hoặc mật khẩu lab.")
        login_user(user)
        _audit_and_trace("login_success", "authentication", "allowed", "credentials_valid", status=303)
        return redirect(url_for("dashboard"), code=303)

    @app.post("/logout")
    @login_required
    def logout():
        failure = _protected_route_checks("logout_csrf_denied", {})
        if failure:
            return failure
        _audit_and_trace(
            "logout_success",
            "secure",
            "allowed",
            "origin_and_token_valid",
            csrf_status="valid",
            origin_status="origin_allowed",
            status=303,
        )
        logout_user()
        return redirect(url_for("index"), code=303)

    @app.get("/dashboard")
    @login_required
    def dashboard():
        return _render("dashboard.html", current_user=_user(), csrf_token=session.get("csrf_token"))

    @app.get("/profile")
    @login_required
    def profile():
        return _render("profile.html", current_user=_user())

    @app.post("/reset-lab")
    @login_required
    def reset_lab():
        before = _user()
        failure = _protected_route_checks("lab_reset_csrf_denied", before)
        if failure:
            return failure
        trace = _audit_and_trace(
            "lab_reset",
            "secure",
            "allowed",
            "origin_and_token_valid",
            csrf_status="valid",
            origin_status="origin_allowed",
            before=before,
            after={"email": "victim_old@lab.local", "demo_balance": 1_000_000},
            status=303,
        )
        reset_database(preserve_evidence=True)
        with transaction() as db:
            _record_state(
                session["user_id"], "lab_reset", before["email"], "victim_old@lab.local",
                request.path, "secure", trace["trace_id"], db,
            )
        logout_user()
        return redirect(url_for("login"), code=303)

    @app.route("/vulnerable/change-email", methods=["GET", "POST"])
    @login_required
    def vulnerable_change_email():
        if request.method == "GET":
            return _render("vulnerable/change_email.html", current_user=_user(), mode="vulnerable")
        before = {"email": _user()["email"]}
        try:
            email = _available_email(request.form.get("email"), session["user_id"])
        except ValidationError as exc:
            return _render("error.html", 400, message=str(exc))
        trace_id = request_trace("vulnerable", "vulnerable_email_changed", state_before=before)["trace_id"]
        with transaction() as db:
            db.execute("UPDATE users SET email = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
                       (email, session["user_id"]))
            _record_state(session["user_id"], "email", before["email"], email, request.path,
                          "vulnerable", trace_id, db)
        action = "vulnerable_email_changed"
        trace = _audit_and_trace(action, "vulnerable", "allowed", "session_cookie_only",
                                 before=before, after={"email": email}, trace_id=trace_id)
        return _render("vulnerable/change_email_result.html", current_user=_user(), trace=trace,
                       state_before=before, state_after={"email": email}, mode="vulnerable")

    @app.route("/secure/change-email", methods=["GET", "POST"])
    @login_required
    def secure_change_email():
        if request.method == "GET":
            return _render("secure/change_email.html", current_user=_user(), csrf_token=session["csrf_token"], mode="secure")
        before = {"email": _user()["email"]}
        origin, csrf_status, failure = _secure_checks("secure_change_email", before)
        if failure:
            return failure
        try:
            email = _available_email(request.form.get("email"), session["user_id"])
        except ValidationError as exc:
            return _render("error.html", 400, message=str(exc))
        trace_id = request_trace("secure", "secure_email_changed", csrf_status=csrf_status,
                                 origin_decision=origin.reason, state_before=before)["trace_id"]
        with transaction() as db:
            db.execute("UPDATE users SET email = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
                       (email, session["user_id"]))
            _record_state(session["user_id"], "email", before["email"], email, request.path, "secure", trace_id, db)
        rotate_csrf_token()
        trace = _audit_and_trace("secure_email_changed", "secure", "allowed", "origin_and_token_valid",
                                 csrf_status="valid", origin_status=origin.reason,
                                 before=before, after={"email": email}, trace_id=trace_id)
        log_event(origin.reason, mode="secure", decision="allowed", reason=origin.reason,
                  csrf_status="valid", trace_id=trace["trace_id"])
        log_event("csrf_token_valid", mode="secure", decision="allowed", reason="token_matches_session",
                  csrf_status="valid", trace_id=trace["trace_id"])
        log_event("csrf_token_rotated", mode="secure", decision="allowed", reason="state_change_completed",
                  csrf_status="rotated", trace_id=trace["trace_id"])
        return _render("secure/change_email_result.html", current_user=_user(), trace=trace,
                       state_before=before, state_after={"email": email}, csrf_token=session["csrf_token"], mode="secure")

    @app.route("/secure/change-password", methods=["GET", "POST"])
    @login_required
    def secure_change_password():
        if request.method == "GET":
            return _render("secure/change_password.html", csrf_token=session["csrf_token"], mode="secure")
        old_hash = query_one("SELECT password_hash FROM users WHERE id = ?", (session["user_id"],))["password_hash"]
        before = {"password_hash_fingerprint": fingerprint(old_hash)}
        origin, csrf_status, failure = _secure_checks("secure_change_password", before)
        if failure:
            return failure
        if not reauthenticate(request.form.get("current_password")):
            trace = _audit_and_trace("password_change_denied", "secure", "denied", "current_password_invalid",
                                     csrf_status=csrf_status, origin_status=origin.reason, before=before,
                                     status=403, reauth_status="failed")
            log_event("reauthentication_failed", mode="secure", decision="denied",
                      reason="current_password_invalid", csrf_status=csrf_status, trace_id=trace["trace_id"])
            return _render("secure/csrf_error.html", 403, reason="current_password_invalid", trace=trace)
        try:
            password = validate_new_password(request.form.get("new_password"))
        except ValidationError as exc:
            return _render("error.html", 400, message=str(exc))
        new_hash = generate_password_hash(password)
        trace_id = request_trace("secure", "password_change_secure", csrf_status=csrf_status,
                                 origin_decision=origin.reason, reauth_status="success")["trace_id"]
        with transaction() as db:
            db.execute("UPDATE users SET password_hash = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now') WHERE id = ?",
                       (new_hash, session["user_id"]))
            _record_state(session["user_id"], "password_hash_fingerprint", fingerprint(old_hash), fingerprint(new_hash),
                          request.path, "secure", trace_id, db)
        rotate_csrf_token()
        trace = _audit_and_trace("password_change_secure", "secure", "allowed", "token_origin_and_password_valid",
                                 csrf_status="valid", origin_status=origin.reason,
                                 before=before, after={"password_hash_fingerprint": fingerprint(new_hash)},
                                 reauth_status="success", trace_id=trace_id)
        log_event("origin_allowed", mode="secure", decision="allowed", reason=origin.reason,
                  csrf_status="valid", trace_id=trace["trace_id"])
        log_event("csrf_token_valid", mode="secure", decision="allowed", reason="token_matches_session",
                  csrf_status="valid", trace_id=trace["trace_id"])
        log_event("reauthentication_success", mode="secure", decision="allowed",
                  reason="current_password_valid", csrf_status="valid", trace_id=trace["trace_id"])
        log_event("csrf_token_rotated", mode="secure", decision="allowed", reason="state_change_completed",
                  csrf_status="rotated", trace_id=trace["trace_id"])
        return _render("secure/change_password.html", message="Mật khẩu demo đã đổi an toàn.", trace=trace,
                       csrf_token=session["csrf_token"], mode="secure")

    @app.route("/secure/transfer", methods=["GET", "POST"])
    @login_required
    def secure_transfer():
        if request.method == "GET":
            return _render("secure/transfer.html", current_user=_user(), csrf_token=session["csrf_token"], mode="secure")
        before = {"sender_balance": _user()["demo_balance"]}
        origin, csrf_status, failure = _secure_checks("secure_transfer", before)
        if failure:
            return failure
        current_password = request.form.get("current_password")
        reauth_ok = is_recently_reauthenticated() or (bool(current_password) and reauthenticate(current_password))
        if not reauth_ok:
            trace = _audit_and_trace("transfer_denied", "secure", "denied", "reauthentication_required",
                                     csrf_status=csrf_status, origin_status=origin.reason, before=before,
                                     status=403, reauth_status="required")
            log_event("reauthentication_failed", mode="secure", decision="denied",
                      reason="reauthentication_required", csrf_status=csrf_status, trace_id=trace["trace_id"])
            return _render("secure/csrf_error.html", 403, reason="reauthentication_required", trace=trace)
        try:
            receiver_id = positive_int(request.form.get("receiver_id"), "receiver_id", 1_000_000)
            amount = positive_int(request.form.get("amount"), "amount", 1_000_000)
            trace_id = request_trace("secure", "transfer_secure", csrf_status=csrf_status,
                                     origin_decision=origin.reason, reauth_status="success")["trace_id"]
            state = _do_transfer(session["user_id"], receiver_id, amount, trace_id)
        except ValidationError as exc:
            trace = _audit_and_trace("transfer_denied", "secure", "denied", str(exc), csrf_status=csrf_status,
                                     origin_status=origin.reason, before=before, status=400, reauth_status="success")
            return _render("error.html", 400, message=str(exc), trace=trace)
        rotate_csrf_token()
        trace = _audit_and_trace("transfer_secure", "secure", "allowed", "token_origin_reauth_and_balance_valid",
                                 csrf_status="valid", origin_status=origin.reason,
                                 reauth_status="success", trace_id=trace_id, **state)
        log_event("origin_allowed", mode="secure", decision="allowed", reason=origin.reason,
                  csrf_status="valid", trace_id=trace["trace_id"])
        log_event("csrf_token_valid", mode="secure", decision="allowed", reason="token_matches_session",
                  csrf_status="valid", trace_id=trace["trace_id"])
        log_event("reauthentication_success", mode="secure", decision="allowed",
                  reason="recent_or_current_password_valid", csrf_status="valid", trace_id=trace["trace_id"])
        log_event("csrf_token_rotated", mode="secure", decision="allowed", reason="state_change_completed",
                  csrf_status="rotated", trace_id=trace["trace_id"])
        return _render("secure/transfer.html", message="Chuyển số dư demo an toàn thành công.", trace=trace,
                       csrf_token=session["csrf_token"], mode="secure")

    @app.get("/comparison")
    def comparison():
        return _render("comparison.html")

    @app.get("/security-controls")
    def security_controls():
        def control(name, status, source, file, routes, risk, limitation):
            return {"name": name, "status": status, "source": source, "file": file,
                    "routes": routes, "risk": risk, "limitation": limitation}
        controls = [
            control("Session authentication", True, "Flask session", "auth.py", "Authenticated routes", "Anonymous mutation", "Signed cookies do not stop CSRF"),
            control("CSRF token", True, "Synchronizer token", "csrf_service.py", "Secure POST routes", "Forged requests", "XSS can read page tokens"),
            control("Token rotation", True, "Runtime session", "csrf_service.py", "Login and secure mutations", "Token reuse", "Rotation does not replace validation"),
            control("Origin validation", True, "Exact allowlist", "origin_service.py", "Secure POST routes", "Cross-origin submissions", "Header can be absent"),
            control("Referer fallback", True, "Exact allowlist", "origin_service.py", "Secure POST routes", "Missing Origin", "Privacy policy may remove Referer"),
            control("SameSite", current_app.config["SESSION_COOKIE_SAMESITE"], "Runtime config", "config.py", "Session cookie", "Some cross-site requests", "Same-site cross-origin remains possible"),
            control("HttpOnly", current_app.config["SESSION_COOKIE_HTTPONLY"], "Runtime config", "config.py", "Session cookie", "JavaScript cookie theft", "Does not stop CSRF"),
            control("Secure cookie", current_app.config["SESSION_COOKIE_SECURE"], "Runtime config", "config.py", "Session cookie", "Cleartext transport", "Disabled for local HTTP lab"),
            control("POST-only state changes", True, "Flask routes", "victim_app.py", "Secure mutations", "Link/prefetch mutation", "POST still needs CSRF protection"),
            control("Input validation", True, "Runtime validators", "security_utils.py", "Email/password/amount", "Malformed input", "Not an authorization check"),
            control("Parameterized SQL", True, "SQLite placeholders", "database.py", "Database writes", "SQL injection", "Does not validate business rules"),
            control("Audit logging", True, "SQLite audit_logs", "audit_service.py", "Security decisions", "Missing accountability", "Local demo retention"),
            control("CSP", bool(CSP), "Response header", "victim_app.py", "All responses", "Script injection impact", "Defense in depth"),
            control("CORS policy", "No wildcard", "Response headers", "victim_app.py", "All responses", "Cross-origin script reads", "CORS is not CSRF protection"),
            control("Request size limit", current_app.config["MAX_CONTENT_LENGTH"], "MAX_CONTENT_LENGTH runtime config", "config.py", "All requests", "Oversized bodies", "Not a rate limit"),
        ]
        return _render("security_controls.html", controls=controls)

    @app.get("/origin-matrix")
    def origin_matrix():
        matrix = [
            {"attacker": "http://127.0.0.1:9004", "same_origin": False, "same_site": True},
            {"attacker": "http://localhost:9004", "same_origin": False, "same_site": False},
        ]
        return _render("origin_matrix.html", matrix=matrix)

    @app.get("/audit-logs")
    @login_required
    def audit_logs():
        return _render("audit_logs.html", logs=list_logs(
            request.args.get("user_id"), request.args.get("action", ""), request.args.get("mode", ""),
            request.args.get("decision", ""), request.args.get("trace_id", ""), request.args.get("username", "")))

    @app.get("/api/trace/<trace_id>")
    @login_required
    def trace_api(trace_id):
        trace = get_trace(trace_id)
        return jsonify(trace) if trace else (jsonify({"error": "trace not found"}), 404)

    @app.post("/api/trace/clear")
    @login_required
    def trace_clear():
        origin, csrf_status, failure = _secure_checks("trace_clear", {})
        if failure:
            return failure
        clear_traces()
        rotate_csrf_token()
        return jsonify({"cleared": True, "csrf_token": session["csrf_token"]})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "Lab04 Victim Application"})

    @app.errorhandler(404)
    def not_found(_error):
        return _render("error.html", 404, message="Không tìm thấy trang.")

    @app.errorhandler(413)
    def too_large(_error):
        return _render("error.html", 413, message="Request body vượt giới hạn 64 KiB.")

    with app.app_context():
        init_db()
        if query_one("SELECT id FROM users LIMIT 1") is None:
            reset_database()
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5004, debug=False)
