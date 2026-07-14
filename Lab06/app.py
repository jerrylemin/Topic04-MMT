from __future__ import annotations

import json
import os
import secrets
import sqlite3
from datetime import UTC, datetime, timedelta
from dataclasses import asdict
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from base64_cookie_service import (
    BASE64_COOKIE,
    Base64Profile,
    authorize_decoded_role,
    decode_profile,
    issue_base64_demo_cookie,
)
from database import UserRecord, connect_database, get_user_by_id, initialize_database
from signed_cookie_service import (
    SIGNED_COOKIE,
    issue_signed_cookie,
    sign_profile,
    verify_signed_profile,
)
from encrypted_cookie_service import (
    demo_encrypted_profile,
    decrypt_demo_profile,
    encrypt_demo_profile,
    issue_encrypted_demo_cookie,
    tamper_encrypted_token,
)
from security_utils import fingerprint, mask_value
from authorization_service import authorize_session_admin
from server_session_service import (
    SESSION_COOKIE,
    expire_session_cookie,
    resolve_session,
    revoke_session,
    rotate_session,
    set_session_cookie,
    revoke_all_demo_sessions,
)
from audit_service import AuditEvent, list_audit_events, record_audit
from config import Config
from seed import seed_database


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 5006


def _connect(path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _initialize_minimal_database(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with _connect(path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('user', 'admin')),
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        now = datetime.now(UTC).isoformat()
        for user in (
            (10, "student", "Sinh viên Demo", "student@lab.local", "Student123!", "user"),
            (1, "admin_lab", "Quản trị Lab", "admin@lab.local", "AdminLab123!", "admin"),
        ):
            existing = connection.execute(
                "SELECT 1 FROM users WHERE id = ?", (user[0],)
            ).fetchone()
            if existing is None:
                connection.execute(
                    """
                    INSERT INTO users
                        (id, username, display_name, email, password_hash, role,
                         active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
                    """,
                    (
                        user[0],
                        user[1],
                        user[2],
                        user[3],
                        generate_password_hash(
                            user[4], method="pbkdf2:sha256:600000"
                        ),
                        user[5],
                        now,
                        now,
                    ),
                )


def _new_trace_legacy(app: Flask, *, mode: str, route: str, decision: str) -> dict[str, Any]:
    trace_id = secrets.token_hex(12)
    now = datetime.now(UTC).isoformat()
    trace = {
        "trace_id": trace_id,
        "mode": mode,
        "route": route,
        "timestamp": now,
        "status": "completed",
        "decision": decision,
        "steps": [
            {
                "step_number": 1,
                "timestamp": now,
                "layer": "HTTP Request",
                "title": "Nhận cookie từ browser",
                "description": "Flask đọc các cookie demo của request local.",
                "technique": "request.cookies",
                "input_data": {"cookie_names": sorted(request.cookies.keys())},
                "output_data": {"mode": mode},
                "code_reference": "app.py:_plain_admin",
                "security_meaning": "Cookie là dữ liệu do client kiểm soát.",
                "status": "observed",
            },
            {
                "step_number": 2,
                "timestamp": now,
                "layer": "Authorization",
                "title": "Quyết định phân quyền",
                "description": f"Vulnerable policy returned {decision}.",
                "technique": "client-role comparison",
                "input_data": {"role": request.cookies.get("lab06_role")},
                "output_data": {"decision": decision},
                "code_reference": "app.py:_plain_admin",
                "security_meaning": "Tin role trong cookie tạo lỗi Broken Access Control.",
                "status": decision,
            },
        ],
    }
    app.extensions["lab06_traces"][trace_id] = trace
    return trace


def _new_trace(app: Flask, *, mode: str, route: str, decision: str) -> dict[str, Any]:
    """Record a truthful, mode-specific trace without exposing cookie values."""
    trace_id = secrets.token_hex(12)
    now = datetime.now(UTC).isoformat()
    cookie_by_mode = {
        "plain": "lab06_role",
        "base64": "lab06_profile_b64",
        "signed": "lab06_signed_profile",
        "encrypted": "lab06_encrypted_profile",
        "session": "lab06_session",
        "server_session": "lab06_session",
    }
    login_details = {
        "plain": ("Cookie issuance", "response.set_cookie", "app.py:login", "The vulnerable model places authorization state in client storage."),
        "base64": ("Base64 profile issuance", "URL-safe Base64 JSON encoding", "base64_cookie_service.py:issue_base64_demo_cookie", "Encoding changes representation but provides no integrity or confidentiality."),
        "signed": ("Signed profile issuance", "HMAC-backed serialization", "signed_cookie_service.py:sign_profile", "A server-held key lets later requests detect payload modification."),
        "server_session": ("Opaque session rotation", "random token plus SHA-256 lookup", "server_session_service.py:rotate_session", "Role and lifecycle remain in server-side state."),
        "session": ("Opaque session rotation", "random token plus SHA-256 lookup", "server_session_service.py:rotate_session", "Role and lifecycle remain in server-side state."),
    }
    request_details = {
        "plain": ("Client-role authorization", "client role comparison", "authorization_service.py:authorize_plain_admin", "Trusting a mutable cookie role creates Broken Access Control."),
        "base64": ("Decode and authorize", "Base64 decode plus client role comparison", "base64_cookie_service.py:authorize_decoded_role", "A reversible encoding does not make authorization data trustworthy."),
        "signed": ("Verify then authorize", "signature verification plus database role lookup", "signed_cookie_service.py:verify_signed_profile", "Integrity is verified before payload use; authorization still uses server state."),
        "encrypted": ("Authenticated decryption", "Fernet authenticated decryption", "encrypted_cookie_service.py:decrypt_demo_profile", "Confidentiality and integrity are demonstrated without payload authorization."),
        "server_session": ("Server-side authorization", "SHA-256 lookup plus database policy", "server_session_service.py:resolve_session", "Revocation, expiry, rotation, and current role remain server-authoritative."),
    }
    details = login_details if route == "/login" else request_details
    title, technique, code_reference, security_meaning = details.get(
        mode,
        ("Fixed local flow", "bounded workflow", "app.py:create_app", "Only Lab06 local behavior is recorded."),
    )
    cookie_name = cookie_by_mode.get(mode)
    trace = {
        "trace_id": trace_id,
        "mode": mode,
        "route": route,
        "timestamp": now,
        "status": "completed",
        "decision": decision,
        "steps": [
            {
                "step_number": 1,
                "timestamp": now,
                "layer": "HTTP Request",
                "title": "Receive fixed Lab06 cookie input",
                "description": "Flask reads only the cookies attached to this local request.",
                "technique": "request.cookies",
                "input_data": {"cookie_names": sorted(request.cookies.keys())},
                "output_data": {"mode": mode, "route": route},
                "code_reference": "app.py:request_boundary",
                "security_meaning": "Cookie input crosses the browser-to-server trust boundary.",
                "status": "observed",
            },
            {
                "step_number": 2,
                "timestamp": now,
                "layer": "Authentication/Authorization",
                "title": title,
                "description": f"Observed the fixed {mode} flow at {route}.",
                "technique": technique,
                "input_data": {
                    "cookie_name": cookie_name,
                    "cookie_present": bool(cookie_name and cookie_name in request.cookies),
                },
                "output_data": {"decision": decision, "mode": mode},
                "code_reference": code_reference,
                "security_meaning": security_meaning,
                "status": decision,
            },
        ],
    }
    app.extensions["lab06_traces"][trace_id] = trace
    return trace


def _record_event(
    app: Flask,
    *,
    action: str,
    route: str,
    mode: str,
    reason: str,
    trace_id: str,
    user_id: int | None = None,
    username: str | None = None,
    cookie_name: str | None = None,
    cookie_status: str | None = None,
    submitted_role: str | None = None,
    database_role: str | None = None,
    decision: str | None = None,
) -> None:
    with connect_database(app.config["DATABASE"]) as connection:
        record_audit(
            connection,
            AuditEvent(
                action=action,
                route=route,
                mode=mode,
                reason=reason,
                trace_id=trace_id,
                user_id=user_id,
                username=username,
                cookie_name=cookie_name,
                cookie_status=cookie_status,
                submitted_role=submitted_role,
                database_role=database_role,
                authorization_decision=decision,
            ),
        )


def _safe_host() -> bool:
    return request.host.split(":", 1)[0] in {"127.0.0.1", "localhost"}


def _source_snippet(filename: str, marker: str) -> dict[str, Any]:
    path = ROOT / filename
    lines = path.read_text(encoding="utf-8").splitlines()
    start_marker = f"# LAB06-CODE:{marker}:START"
    end_marker = f"# LAB06-CODE:{marker}:END"
    starts = [index for index, line in enumerate(lines) if line.strip() == start_marker]
    ends = [index for index, line in enumerate(lines) if line.strip() == end_marker]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        raise RuntimeError(f"Invalid source marker registry entry: {filename}:{marker}")
    return {
        "file": filename,
        "function": marker,
        "line_start": starts[0] + 2,
        "line_end": ends[0],
        "source": "\n".join(lines[starts[0] + 1 : ends[0]]),
    }


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    ephemeral_secret = secrets.token_urlsafe(32)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("LAB06_SECRET_KEY", ephemeral_secret),
        SIGNING_KEY=os.environ.get("LAB06_SIGNING_KEY", Config.SIGNING_KEY),
        FERNET_KEY=os.environ.get("LAB06_FERNET_KEY", Config.FERNET_KEY),
        DATABASE=os.environ.get(
            "LAB06_DATABASE", str(ROOT / "data" / "lab06.sqlite3")
        ),
        COOKIE_SECURE=os.environ.get("LAB06_COOKIE_SECURE", "false").lower()
        in {"1", "true", "yes"},
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_TTL_SECONDS=30 * 60,
        DEBUG=False,
    )
    if test_config:
        app.config.update(test_config)
    app.extensions["lab06_traces"] = {}
    _initialize_minimal_database(app.config["DATABASE"])
    schema_connection = connect_database(app.config["DATABASE"])
    try:
        initialize_database(schema_connection)
    finally:
        schema_connection.close()

    @app.before_request
    def enforce_local_host() -> Response | None:
        if not _safe_host():
            return Response("Host không được phép trong lab local.", status=400)
        return None

    @app.after_request
    def add_security_headers(response: Response) -> Response:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
        )
        if request.path in {"/login", "/audit-logs"} or "admin" in request.path:
            response.headers["Cache-Control"] = "no-store, max-age=0"
        return response

    @app.get("/")
    def index() -> str:
        return render_template("index.html", title="LAB 6 - Cookie Poisoning")

    @app.get("/health")
    def health() -> Response:
        return jsonify(status="ok", host=HOST, port=PORT, debug=False)

    @app.route("/login", methods=["GET", "POST"])
    def login() -> str | Response:
        if request.method == "GET":
            return render_template("login.html", title="Đăng nhập demo")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        mode = request.form.get("mode", "")
        if mode not in {"plain", "base64", "signed", "session"}:
            return render_template("error.html", title="Chế độ không hợp lệ"), 400
        with _connect(app.config["DATABASE"]) as connection:
            user = connection.execute(
                "SELECT * FROM users WHERE username = ? AND active = 1", (username,)
            ).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            failed_trace = _new_trace(
                app, mode=mode or "unknown", route="/login", decision="deny"
            )
            _record_event(
                app,
                action="login_failed",
                route="/login",
                mode=mode or "unknown",
                reason="invalid_credentials",
                trace_id=failed_trace["trace_id"],
                username=username or None,
                decision="deny",
            )
            return render_template("error.html", title="Đăng nhập thất bại"), 401
        if mode == "base64":
            login_trace = _new_trace(
                app, mode="base64", route="/login", decision="cookie_issued"
            )
            response = redirect(url_for("base64_profile"))
            issue_base64_demo_cookie(
                response,
                app.config,
                Base64Profile(username=user["username"], role=user["role"]),
            )
            _record_event(
                app, action="base64_cookie_issued", route="/login", mode="base64",
                reason="fixed_demo_profile", trace_id=login_trace["trace_id"],
                user_id=int(user["id"]), username=str(user["username"]),
                cookie_name=BASE64_COOKIE, cookie_status="issued", submitted_role=str(user["role"]),
                database_role=str(user["role"]), decision="allow",
            )
            return response
        if mode == "signed":
            signed_user = UserRecord(
                id=int(user["id"]),
                username=str(user["username"]),
                display_name=str(user["display_name"]),
                email=str(user["email"]),
                password_hash=str(user["password_hash"]),
                role=str(user["role"]),
                active=bool(user["active"]),
                created_at=str(user["created_at"]),
                updated_at=str(user["updated_at"]),
            )
            token = sign_profile(signed_user, app.config, datetime.now(UTC))
            response = redirect(url_for("signed_profile"))
            issue_signed_cookie(response, token, app.config)
            login_trace = _new_trace(
                app, mode="signed", route="/login", decision="cookie_issued"
            )
            _record_event(
                app, action="signed_cookie_issued", route="/login", mode="signed",
                reason="signed_profile_created", trace_id=login_trace["trace_id"],
                user_id=signed_user.id, username=signed_user.username,
                cookie_name=SIGNED_COOKIE, cookie_status="issued",
                submitted_role=signed_user.role, database_role=signed_user.role, decision="allow",
            )
            return response
        if mode == "session":
            trace = _new_trace(
                app, mode="session", route="/login", decision="session_created"
            )
            with connect_database(app.config["DATABASE"]) as connection:
                issue = rotate_session(
                    connection,
                    user_id=int(user["id"]),
                    previous_raw_token=request.cookies.get(SESSION_COOKIE),
                    now=datetime.now(UTC),
                    ttl=timedelta(seconds=int(app.config["SESSION_TTL_SECONDS"])),
                    trace_id=trace["trace_id"],
                    reason="login_rotation",
                )
            response = redirect(url_for("session_profile"))
            set_session_cookie(response, issue, app.config)
            response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
            response.headers["X-Lab-Session-Status"] = issue.rotation_reason
            _record_event(
                app, action="server_session_rotated" if request.cookies.get(SESSION_COOKIE) else "server_session_created",
                route="/login", mode="server_session", reason="login_rotation",
                trace_id=trace["trace_id"], user_id=int(user["id"]),
                username=str(user["username"]), cookie_name=SESSION_COOKIE,
                cookie_status="issued", database_role=str(user["role"]), decision="allow",
            )
            return response
        if mode != "plain":
            return redirect(url_for("dashboard"))
        response = redirect(url_for("plain_profile"))
        common = {
            "path": "/",
            "samesite": "Lax",
            "secure": bool(app.config["COOKIE_SECURE"]),
            "httponly": False,
        }
        response.set_cookie("lab06_username", user["username"], **common)
        response.set_cookie("lab06_role", user["role"], **common)
        login_trace = _new_trace(app, mode="plain", route="/login", decision="cookie_issued")
        _record_event(
            app, action="plain_cookie_issued", route="/login", mode="plain",
            reason="fixed_plain_demo", trace_id=login_trace["trace_id"],
            user_id=int(user["id"]), username=str(user["username"]),
            cookie_name="lab06_role", cookie_status="issued",
            submitted_role=str(user["role"]), database_role=str(user["role"]), decision="allow",
        )
        return response

    @app.get("/dashboard")
    def dashboard() -> str:
        return render_template("dashboard.html", title="Dashboard")

    @app.get("/comparison")
    def comparison() -> str:
        models = [
            {"name": "Plain Cookie", "integrity": "Không", "confidentiality": "Không", "authorization": "Client role (lỗi)"},
            {"name": "Base64 Cookie", "integrity": "Không", "confidentiality": "Không", "authorization": "Decoded client role (lỗi)"},
            {"name": "Signed Cookie", "integrity": "Có", "confidentiality": "Không", "authorization": "Database role"},
            {"name": "Encrypted Cookie", "integrity": "Có", "confidentiality": "Có", "authorization": "Không dùng"},
            {"name": "Server-side Session", "integrity": "Opaque token", "confidentiality": "State ở server", "authorization": "Database role"},
        ]
        code_comparison = {
            "vulnerable": {
                **_source_snippet("authorization_service.py", "plain_authorization"),
                "explanation": "Tin lab06_role do client gửi.",
            },
            "secure": {
                **_source_snippet("authorization_service.py", "session_database_authorization"),
                "explanation": "Lấy role hiện tại từ database qua server session.",
            },
        }
        return render_template(
            "comparison.html",
            title="So sánh năm mô hình",
            rows=models,
            trace={"code_comparison": code_comparison},
        )

    @app.get("/security-controls")
    def security_controls_page() -> str:
        controls = [
            {"name": "Opaque Session ID", "status": "enabled", "source": "server_session_service.py"},
            {"name": "Database role lookup", "status": "enabled", "source": "database.py"},
            {"name": "Session rotation", "status": "enabled", "source": "server_session_service.py"},
            {"name": "Server-side logout invalidation", "status": "enabled", "source": "server_session_service.py"},
            {"name": "Signed cookie integrity", "status": "enabled", "source": "signed_cookie_service.py"},
            {"name": "Authenticated encryption", "status": "enabled", "source": "encrypted_cookie_service.py"},
            {"name": "HttpOnly", "status": "secure flows only", "source": "config.cookie_options"},
            {"name": "Secure", "status": str(bool(app.config["COOKIE_SECURE"])).lower(), "source": "LAB06_COOKIE_SECURE"},
            {"name": "SameSite", "status": "Lax", "source": "config.cookie_options"},
            {"name": "PBKDF2", "status": "600000 iterations", "source": "seed.py"},
            {"name": "Parameterized SQL", "status": "enabled", "source": "database.py"},
            {"name": "CSP", "status": "enabled", "source": "app.after_request"},
            {"name": "Request size", "status": str(app.config["MAX_CONTENT_LENGTH"]), "source": "Flask config"},
        ]
        return render_template(
            "security_controls.html",
            title="Security Control Panel",
            rows=controls,
            security_controls=controls,
        )

    @app.get("/audit-logs")
    def audit_logs_page() -> str:
        with connect_database(app.config["DATABASE"]) as connection:
            rows = [record.to_dict() for record in list_audit_events(connection)]
        return render_template("audit_logs.html", title="Audit logs", rows=rows)

    @app.get("/vulnerable/plain/profile")
    def plain_profile() -> str:
        return render_template(
            "vulnerable/plain_profile.html",
            title="Plain Cookie Profile",
            result={
                "username": request.cookies.get("lab06_username"),
                "role": request.cookies.get("lab06_role"),
            },
        )

    # LAB06-CODE:plain_route_authorization:START
    @app.get("/vulnerable/plain/admin")
    def plain_admin() -> tuple[str, int] | str:
        username = request.cookies.get("lab06_username")
        role = request.cookies.get("lab06_role")
        allowed = role == "admin"
        decision = "allow" if allowed else "deny"
        trace = _new_trace(
            app, mode="plain", route="/vulnerable/plain/admin", decision=decision
        )
        template = (
            "vulnerable/plain_admin.html"
            if allowed
            else "vulnerable/plain_denied.html"
        )
        body = render_template(
            template,
            title="Plain Cookie Admin",
            result={"username": username, "role": role},
            trace=trace,
            verdict={
                "decision": decision,
                "root_cause": "Server tin cookie phía client.",
            },
        )
        response = app.make_response((body, 200 if allowed else 403))
        response.headers["X-Lab-Decision"] = decision
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        action = "plain_admin_allowed_from_cookie" if allowed else "plain_admin_denied"
        if role == "admin" and username == "student":
            action = "plain_cookie_role_changed_observed"
        _record_event(
            app, action=action, route="/vulnerable/plain/admin", mode="plain",
            reason="client_cookie_role_used", trace_id=trace["trace_id"],
            username=username, cookie_name="lab06_role", cookie_status="observed",
            submitted_role=role, decision=decision,
        )
        return response
    # LAB06-CODE:plain_route_authorization:END

    @app.get("/vulnerable/base64/profile")
    def base64_profile() -> tuple[str, int] | str:
        decoded = decode_profile(request.cookies.get(BASE64_COOKIE))
        if not decoded.valid:
            return render_template(
                "vulnerable/base64_denied.html", result=asdict(decoded)
            ), 400
        return render_template(
            "vulnerable/base64_profile.html",
            title="Base64 Cookie Profile",
            result=asdict(decoded),
        )

    @app.get("/vulnerable/base64/admin")
    def base64_admin() -> Response:
        decoded = decode_profile(request.cookies.get(BASE64_COOKIE))
        if not decoded.valid:
            trace = _new_trace(
                app,
                mode="base64",
                route="/vulnerable/base64/admin",
                decision="invalid",
            )
            trace["inspectors"] = {
                "base64": {
                    "algorithm": "URL-safe Base64",
                    "parse_result": decoded.reason,
                    "integrity": False,
                    "confidentiality": False,
                }
            }
            body = render_template(
                "vulnerable/base64_denied.html", result=asdict(decoded), trace=trace
            )
            response = app.make_response((body, 400))
            response.headers["X-Lab-Decision"] = "invalid"
            response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
            _record_event(
                app, action="base64_decode_failed", route="/vulnerable/base64/admin",
                mode="base64", reason=decoded.reason, trace_id=trace["trace_id"],
                cookie_name=BASE64_COOKIE, cookie_status="invalid", decision="deny",
            )
            return response
        allowed = authorize_decoded_role(decoded)
        decision = "allow" if allowed else "deny"
        trace = _new_trace(
            app,
            mode="base64",
            route="/vulnerable/base64/admin",
            decision=decision,
        )
        trace["inspectors"] = {
            "base64": {
                "algorithm": "URL-safe Base64",
                "decoded_json": decoded.decoded_json,
                "role_extracted": decoded.profile.role,
                "parse_result": decoded.reason,
                "integrity": False,
                "confidentiality": False,
                "authorization_result": decision,
            }
        }
        template = (
            "vulnerable/base64_admin.html"
            if allowed
            else "vulnerable/base64_denied.html"
        )
        body = render_template(template, result=asdict(decoded), trace=trace)
        response = app.make_response((body, 200 if allowed else 403))
        response.headers["X-Lab-Decision"] = decision
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        _record_event(
            app,
            action="base64_admin_allowed_from_cookie" if allowed else "base64_decode_success",
            route="/vulnerable/base64/admin", mode="base64",
            reason="decoded_role_used_without_signature", trace_id=trace["trace_id"],
            username=decoded.profile.username, cookie_name=BASE64_COOKIE,
            cookie_status="decoded", submitted_role=decoded.profile.role, decision=decision,
        )
        return response

    def _signed_result_response(*, admin: bool) -> Response:
        verified = verify_signed_profile(request.cookies.get(SIGNED_COOKIE), app.config)
        route = "/secure/signed/admin" if admin else "/secure/signed/profile"
        if not verified.valid:
            status = 401 if verified.signature_status == "missing" else 400
            trace = _new_trace(
                app, mode="signed", route=route, decision=verified.signature_status
            )
            trace["inspectors"] = {
                "signature": {
                    "signature_status": verified.signature_status,
                    "reason": verified.reason,
                    "payload_used": False,
                    "integrity": True,
                    "confidentiality": False,
                }
            }
            body = render_template(
                "secure/signed_invalid.html", result=asdict(verified), trace=trace
            )
            response = app.make_response((body, status))
            response.headers["X-Lab-Signature-Status"] = verified.signature_status
            response.headers["X-Lab-Decision"] = "deny"
            response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
            _record_event(
                app, action="signed_cookie_invalid", route=route, mode="signed",
                reason=verified.reason, trace_id=trace["trace_id"],
                cookie_name=SIGNED_COOKIE, cookie_status=verified.signature_status, decision="deny",
            )
            return response
        payload = verified.payload
        database_user = None
        with connect_database(app.config["DATABASE"]) as connection:
            database_user = get_user_by_id(connection, payload.user_id)
        allowed = bool(database_user and database_user.active)
        if admin:
            allowed = bool(allowed and database_user.role == "admin")
        decision = "allow" if allowed else "deny"
        trace = _new_trace(app, mode="signed", route=route, decision=decision)
        trace["inspectors"] = {
            "signature": {
                "signature_status": "valid",
                "reason": verified.reason,
                "payload_used": True,
                "signed_role": payload.role,
                "integrity": True,
                "confidentiality": False,
            },
            "authorization": {
                "subject": payload.username,
                "authentication_source": "verified signed cookie",
                "requested_action": "view_admin" if admin else "view_profile",
                "requested_resource": route,
                "submitted_role": payload.role,
                "database_role": database_user.role if database_user else None,
                "policy": "current database role must equal admin" if admin else "active database user required",
                "decision": decision,
                "reason": "Role is read from SQLite after signature verification.",
            },
        }
        template = (
            "secure/signed_admin.html"
            if admin and allowed
            else "secure/signed_invalid.html"
            if admin
            else "secure/signed_profile.html"
        )
        body = render_template(
            template,
            result={"title": "Signed cookie verified", "message": verified.reason},
            user=asdict(database_user) if database_user else {},
            trace=trace,
        )
        response = app.make_response((body, 200 if allowed else 403))
        response.headers["X-Lab-Signature-Status"] = "valid"
        response.headers["X-Lab-Decision"] = decision
        response.headers["X-Lab-Role-Source"] = "database"
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        _record_event(
            app, action="signed_cookie_valid", route=route, mode="signed",
            reason="signature_verified_then_database_role_checked", trace_id=trace["trace_id"],
            user_id=database_user.id if database_user else None,
            username=database_user.username if database_user else payload.username,
            cookie_name=SIGNED_COOKIE, cookie_status="valid", submitted_role=payload.role,
            database_role=database_user.role if database_user else None, decision=decision,
        )
        return response

    @app.get("/secure/signed/profile")
    def signed_profile() -> Response:
        return _signed_result_response(admin=False)

    @app.get("/secure/signed/admin")
    def signed_admin() -> Response:
        return _signed_result_response(admin=True)

    @app.get("/secure/encrypted-demo")
    def encrypted_demo() -> Response:
        profile = demo_encrypted_profile(datetime.now(UTC))
        token = encrypt_demo_profile(profile, app.config)
        verified = decrypt_demo_profile(token, app.config)
        tampered = decrypt_demo_profile(tamper_encrypted_token(token), app.config)
        trace = _new_trace(
            app,
            mode="encrypted",
            route="/secure/encrypted-demo",
            decision="read_only_demo",
        )
        trace["inspectors"] = {
            "encryption": {
                "algorithm": "Fernet authenticated encryption",
                "masked_token": mask_value(token),
                "token_fingerprint": fingerprint(token),
                "decrypt_result": verified.reason,
                "tamper_detection_result": tampered.reason,
                "confidentiality": True,
                "integrity": True,
                "key_location": "server environment only",
                "authorization_used": False,
            }
        }
        body = render_template(
            "secure/encrypted_demo.html",
            result={
                "title": "Encrypted Cookie Demo",
                "message": "Authenticated encryption che nội dung và phát hiện thay đổi.",
            },
            demo_values={
                "encrypted_purpose": "read_only_cookie_demo",
                "encrypted_payload_summary": "user_id + display_name + preference + issued_at",
            },
            trace=trace,
        )
        response = app.make_response(body)
        issue_encrypted_demo_cookie(response, token, app.config)
        response.headers["X-Lab-Authorization-Used"] = "false"
        response.headers["X-Lab-Encryption-Status"] = verified.encryption_status
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        _record_event(
            app, action="encrypted_demo_generated", route="/secure/encrypted-demo",
            mode="encrypted", reason="fernet_read_only_demo", trace_id=trace["trace_id"],
            cookie_name="lab06_encrypted_profile", cookie_status="valid", decision="not_used",
        )
        return response

    def _resolve_current_session():
        connection = connect_database(app.config["DATABASE"])
        try:
            resolution = resolve_session(
                connection,
                request.cookies.get(SESSION_COOKIE),
                datetime.now(UTC),
            )
        finally:
            connection.close()
        return resolution

    @app.get("/secure/session/profile")
    def session_profile() -> Response:
        resolution = _resolve_current_session()
        decision = "allow" if resolution.valid else "deny"
        trace = _new_trace(
            app,
            mode="server_session",
            route="/secure/session/profile",
            decision=decision,
        )
        trace["inspectors"] = {
            "session": {
                "cookie_name": SESSION_COOKIE,
                "cookie_present": bool(request.cookies.get(SESSION_COOKIE)),
                "masked_session_id": mask_value(request.cookies.get(SESSION_COOKIE)),
                "token_fingerprint": resolution.token_fingerprint,
                "hash_algorithm": "SHA-256",
                "server_record_found": resolution.session_id is not None,
                "session_active": resolution.active,
                "created_at": resolution.created_at,
                "expires_at": resolution.expires_at,
                "last_seen_at": resolution.last_seen_at,
                "user_id": resolution.user_id,
                "username": resolution.username,
                "database_role": resolution.database_role,
                "authorization_decision": decision,
                "reason": resolution.reason,
            }
        }
        template = (
            "secure/session_profile.html"
            if resolution.valid
            else "secure/session_denied.html"
        )
        body = render_template(
            template,
            result={
                "title": "Server-side session",
                "message": resolution.reason,
            },
            user={
                "id": resolution.user_id,
                "username": resolution.username,
                "role": resolution.database_role,
            },
            trace=trace,
        )
        response = app.make_response((body, 200 if resolution.valid else 401))
        response.headers["X-Lab-Decision"] = decision
        response.headers["X-Lab-Session-Status"] = resolution.reason
        response.headers["X-Lab-Role-Source"] = "database"
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        _record_event(
            app, action="server_session_valid" if resolution.valid else "server_session_invalid",
            route="/secure/session/profile", mode="server_session", reason=resolution.reason,
            trace_id=trace["trace_id"], user_id=resolution.user_id,
            username=resolution.username, cookie_name=SESSION_COOKIE,
            cookie_status=resolution.reason, database_role=resolution.database_role,
            decision=decision,
        )
        return response

    @app.get("/secure/session/admin")
    def session_admin() -> Response:
        resolution = _resolve_current_session()
        authz = authorize_session_admin(resolution)
        trace = _new_trace(
            app,
            mode="server_session",
            route="/secure/session/admin",
            decision=authz.decision,
        )
        trace["inspectors"] = {
            "authorization": asdict(authz),
            "session": {
                "cookie_name": SESSION_COOKIE,
                "masked_session_id": mask_value(request.cookies.get(SESSION_COOKIE)),
                "token_fingerprint": resolution.token_fingerprint,
                "server_record_found": resolution.session_id is not None,
                "session_active": resolution.active,
                "username": resolution.username,
                "database_role": resolution.database_role,
                "reason": resolution.reason,
            },
        }
        if not resolution.valid:
            status = 401
        else:
            status = 200 if authz.allowed else 403
        template = (
            "secure/session_admin.html"
            if authz.allowed
            else "secure/session_denied.html"
        )
        body = render_template(
            template,
            result={"title": "Server-side authorization", "message": authz.reason},
            user={"username": resolution.username, "role": resolution.database_role},
            trace=trace,
        )
        response = app.make_response((body, status))
        response.headers["X-Lab-Decision"] = authz.decision
        response.headers["X-Lab-Session-Status"] = resolution.reason
        response.headers["X-Lab-Role-Source"] = "database"
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        _record_event(
            app, action="authorization_allowed" if authz.allowed else "authorization_denied",
            route="/secure/session/admin", mode="server_session", reason=authz.reason,
            trace_id=trace["trace_id"], user_id=resolution.user_id,
            username=resolution.username, cookie_name=SESSION_COOKIE,
            cookie_status=resolution.reason, database_role=resolution.database_role,
            decision=authz.decision,
        )
        return response

    def _logout_response() -> Response:
        trace = _new_trace(
            app, mode="server_session", route=request.path, decision="logout"
        )
        with connect_database(app.config["DATABASE"]) as connection:
            revoked = revoke_session(
                connection,
                raw_token=request.cookies.get(SESSION_COOKIE),
                now=datetime.now(UTC),
                reason="user_logout",
                trace_id=trace["trace_id"],
            )
        body = render_template(
            "secure/session_denied.html",
            result={
                "title": "Logout hoàn tất",
                "message": "Session phía server đã bị thu hồi." if revoked else "Không có session active.",
            },
            trace=trace,
        )
        response = app.make_response(body)
        expire_session_cookie(response, app.config)
        response.headers["X-Lab-Session-Status"] = (
            "logout_invalidated_session" if revoked else "no_active_session"
        )
        response.headers["X-Lab-Trace-ID"] = trace["trace_id"]
        _record_event(
            app, action="logout_invalidated_session" if revoked else "logout_success",
            route=request.path, mode="server_session",
            reason="server_side_record_revoked" if revoked else "no_active_session",
            trace_id=trace["trace_id"], cookie_name=SESSION_COOKIE,
            cookie_status="expired", decision="allow",
        )
        return response

    @app.post("/secure/session/logout")
    def secure_session_logout() -> Response:
        return _logout_response()

    @app.post("/logout")
    def logout() -> Response:
        return _logout_response()

    @app.post("/reset-lab")
    def reset_lab() -> Response:
        trace = _new_trace(app, mode="control", route="/reset-lab", decision="reset")
        seed_database(app.config["DATABASE"])
        with connect_database(app.config["DATABASE"]) as connection:
            revoked = revoke_all_demo_sessions(
                connection, now=datetime.now(UTC), trace_id=trace["trace_id"]
            )
        _record_event(
            app, action="lab_reset", route="/reset-lab", mode="control",
            reason=f"revoked_sessions={revoked}", trace_id=trace["trace_id"], decision="allow",
        )
        response = jsonify(status="reset", revoked_sessions=revoked, trace_id=trace["trace_id"])
        expire_session_cookie(response, app.config)
        return response

    @app.post("/api/trace/clear")
    def clear_trace_api() -> Response:
        count = len(app.extensions["lab06_traces"])
        app.extensions["lab06_traces"].clear()
        return jsonify(status="cleared", count=count)

    @app.get("/api/trace/<trace_id>")
    def trace_api(trace_id: str) -> Response:
        trace = app.extensions["lab06_traces"].get(trace_id)
        if trace is None:
            return jsonify(error="trace_not_found"), 404
        return app.response_class(
            json.dumps(trace, ensure_ascii=False),
            status=200,
            mimetype="application/json",
        )

    return app


if __name__ == "__main__":
    create_app().run(host=HOST, port=PORT, debug=False)
