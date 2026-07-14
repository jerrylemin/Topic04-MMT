"""Run fixed Lab06 Flask flows and export only observed, redacted evidence."""

from __future__ import annotations

import json
import re
import secrets
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app  # noqa: E402
from base64_cookie_service import (  # noqa: E402
    BASE64_COOKIE,
    encode_profile,
    modified_demo_profile,
)
from database import connect_database  # noqa: E402
from encrypted_cookie_service import ENCRYPTED_COOKIE  # noqa: E402
from security_utils import fingerprint, mask_value, redact  # noqa: E402
from server_session_service import SESSION_COOKIE  # noqa: E402
from signed_cookie_service import SIGNED_COOKIE  # noqa: E402
from reset_database import DATABASE, reset_database  # noqa: E402


EVIDENCE = ROOT / "evidence"
COOKIE_NAMES = (
    "lab06_username",
    "lab06_role",
    BASE64_COOKIE,
    SIGNED_COOKIE,
    ENCRYPTED_COOKIE,
    SESSION_COOKIE,
)
DEMO_PASSWORDS = ("Student123!", "AdminLab123!")
FULL_HEX_SECRET = re.compile(r"\b[a-f0-9]{64}\b", re.IGNORECASE)
SAFE_RESPONSE_HEADERS = (
    "Content-Type",
    "Location",
    "X-Lab-Decision",
    "X-Lab-Trace-ID",
    "X-Lab-Role-Source",
    "X-Lab-Signature-Status",
    "X-Lab-Encryption-Status",
    "X-Lab-Authorization-Used",
    "X-Lab-Session-Status",
)


@dataclass(slots=True)
class Capture:
    name: str
    request: dict[str, Any]
    response: dict[str, Any]
    trace: dict[str, Any]
    cookies: list[dict[str, Any]]


def _write_json(path: Path, value: Any) -> None:
    clean = redact(value)
    _assert_redacted(clean)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(clean, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_text(path: Path, value: Any) -> None:
    clean = redact(value)
    _assert_redacted(clean)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(clean, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _assert_redacted(value: Any) -> None:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if any(password in text for password in DEMO_PASSWORDS):
        raise RuntimeError("Evidence contains a plaintext demo password")
    if FULL_HEX_SECRET.search(text):
        raise RuntimeError("Evidence contains a full 64-character hash or secret")


def _cookie_from_client(client: Any, name: str):
    for domain in ("127.0.0.1", "localhost"):
        cookie = client.get_cookie(name, domain=domain)
        if cookie is not None:
            return cookie
    return None


def _client_cookie_evidence(client: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for name in COOKIE_NAMES:
        cookie = _cookie_from_client(client, name)
        if cookie is None:
            continue
        value = str(cookie.value)
        records.append(
            {
                "name": name,
                "masked_value": mask_value(value),
                "value_fingerprint": fingerprint(value),
                "domain": cookie.domain,
                "path": cookie.path,
                "secure": bool(cookie.secure),
                "httponly": bool(cookie.http_only),
                "samesite": cookie.same_site,
            }
        )
    return records


def _set_cookie_evidence(response: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for header in response.headers.getlist("Set-Cookie"):
        parsed = SimpleCookie()
        parsed.load(header)
        for name, morsel in parsed.items():
            value = morsel.value
            records.append(
                {
                    "name": name,
                    "masked_value": mask_value(value),
                    "value_fingerprint": fingerprint(value),
                    "path": morsel["path"] or "/",
                    "domain": morsel["domain"] or "host-only",
                    "secure": bool(morsel["secure"]),
                    "httponly": bool(morsel["httponly"]),
                    "samesite": morsel["samesite"] or None,
                    "max_age": morsel["max-age"] or None,
                }
            )
    return records


def _latest_trace_id(action: str) -> str | None:
    connection = connect_database(DATABASE)
    try:
        row = connection.execute(
            "SELECT trace_id FROM audit_logs WHERE action = ? ORDER BY id DESC LIMIT 1",
            (action,),
        ).fetchone()
    finally:
        connection.close()
    return str(row["trace_id"]) if row else None


def _request_evidence(response: Any, trace: dict[str, Any]) -> dict[str, Any]:
    observed = response.request
    try:
        form_values = {
            key: "[REDACTED]" if key.lower() == "password" else value
            for key, value in observed.form.items()
        }
    except Exception:
        form_values = {}
    return {
        "method": observed.method,
        "scheme": observed.scheme,
        "host": observed.host,
        "path": observed.path,
        "query_string": observed.query_string.decode("utf-8", errors="replace"),
        "content_type": observed.content_type,
        "content_length": observed.content_length or 0,
        "form_field_names": sorted(form_values),
        "form_values": form_values,
        "trace_id": trace.get("trace_id"),
        "observed_at": trace.get("timestamp", datetime.now(UTC).isoformat()),
    }


def _response_evidence(response: Any, trace: dict[str, Any]) -> dict[str, Any]:
    return {
        "status_code": response.status_code,
        "headers": {
            name: response.headers[name]
            for name in SAFE_RESPONSE_HEADERS
            if name in response.headers
        },
        "set_cookie_names": [item["name"] for item in _set_cookie_evidence(response)],
        "trace_id": trace.get("trace_id"),
        "decision": response.headers.get("X-Lab-Decision", trace.get("decision")),
    }


def _capture(
    app: Any,
    client: Any,
    name: str,
    method: str,
    path: str,
    *,
    audit_action: str | None = None,
    **kwargs: Any,
) -> Capture:
    response = getattr(client, method)(path, **kwargs)
    trace_id = response.headers.get("X-Lab-Trace-ID")
    if not trace_id and audit_action:
        trace_id = _latest_trace_id(audit_action)
    if not trace_id:
        raise RuntimeError(f"Flow {name} produced no real trace identifier")
    trace_response = client.get(f"/api/trace/{trace_id}")
    if trace_response.status_code != 200:
        raise RuntimeError(f"Flow {name} trace {trace_id} was not retrievable")
    trace = trace_response.get_json()
    if not isinstance(trace, dict) or trace.get("trace_id") != trace_id:
        raise RuntimeError(f"Flow {name} returned an invalid trace payload")
    cookies = _set_cookie_evidence(response) + _client_cookie_evidence(client)
    capture = Capture(
        name=name,
        request=_request_evidence(response, trace),
        response=_response_evidence(response, trace),
        trace=trace,
        cookies=cookies,
    )
    _assert_redacted(
        {
            "request": capture.request,
            "response": capture.response,
            "trace": capture.trace,
            "cookies": capture.cookies,
        }
    )
    return capture


def _mutate_one_character(value: str) -> str:
    if not value:
        raise RuntimeError("Cannot mutate an empty fixed demo token")
    index = max(1, len(value) // 2)
    replacement = "A" if value[index] != "A" else "B"
    return value[:index] + replacement + value[index + 1 :]


def _login(client: Any, username: str, password: str, mode: str, **extra: Any):
    return client.post(
        "/login",
        data={"username": username, "password": password, "mode": mode},
        follow_redirects=False,
        **extra,
    )


def build_fixed_app():
    reset_database()
    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(DATABASE),
            "SECRET_KEY": secrets.token_urlsafe(48),
            "SIGNING_KEY": secrets.token_urlsafe(48),
            "FERNET_KEY": Fernet.generate_key().decode("ascii"),
            "COOKIE_SECURE": False,
            "SERVER_NAME": "127.0.0.1:5006",
        }
    )


def run_fixed_flows() -> tuple[Any, list[Capture]]:
    app = build_fixed_app()
    captures: list[Capture] = []

    plain = app.test_client()
    captures.append(_capture(app, plain, "plain_cookie_login", "post", "/login",
        audit_action="plain_cookie_issued",
        data={"username": "student", "password": "Student123!", "mode": "plain"},
        follow_redirects=False))
    captures.append(_capture(app, plain, "plain_admin_denied", "get", "/vulnerable/plain/admin"))
    plain.set_cookie("lab06_role", "admin", domain="127.0.0.1")
    captures.append(_capture(app, plain, "plain_cookie_modified", "get", "/vulnerable/plain/admin"))

    base64_client = app.test_client()
    captures.append(_capture(app, base64_client, "base64_cookie_login", "post", "/login",
        audit_action="base64_cookie_issued",
        data={"username": "student", "password": "Student123!", "mode": "base64"},
        follow_redirects=False))
    captures.append(_capture(app, base64_client, "base64_original", "get", "/vulnerable/base64/admin"))
    base64_client.set_cookie(
        BASE64_COOKIE,
        encode_profile(modified_demo_profile()),
        domain="127.0.0.1",
    )
    captures.append(_capture(app, base64_client, "base64_modified", "get", "/vulnerable/base64/admin"))

    signed = app.test_client()
    captures.append(_capture(app, signed, "signed_cookie_login", "post", "/login",
        audit_action="signed_cookie_issued",
        data={"username": "admin_lab", "password": "AdminLab123!", "mode": "signed"},
        follow_redirects=False))
    captures.append(_capture(app, signed, "signed_cookie_valid", "get", "/secure/signed/admin"))
    signed_cookie = _cookie_from_client(signed, SIGNED_COOKIE)
    if signed_cookie is None:
        raise RuntimeError("Signed login did not issue the fixed signed cookie")
    signed.set_cookie(
        SIGNED_COOKIE,
        _mutate_one_character(str(signed_cookie.value)),
        domain="127.0.0.1",
    )
    captures.append(_capture(app, signed, "signed_cookie_invalid", "get", "/secure/signed/profile"))

    encrypted = app.test_client()
    captures.append(_capture(
        app,
        encrypted,
        "encrypted_cookie_valid_and_tampered",
        "get",
        "/secure/encrypted-demo",
    ))

    student = app.test_client()
    captures.append(_capture(app, student, "server_session_student_login", "post", "/login",
        data={"username": "student", "password": "Student123!", "mode": "session"},
        follow_redirects=False))
    captures.append(_capture(app, student, "student_admin_denied", "get", "/secure/session/admin"))
    first_session = _cookie_from_client(student, SESSION_COOKIE)
    if first_session is None:
        raise RuntimeError("Student login did not issue the fixed server session cookie")
    first_raw = str(first_session.value)
    captures.append(_capture(app, student, "session_rotation", "post", "/login",
        data={"username": "student", "password": "Student123!", "mode": "session"},
        follow_redirects=False))
    rotated_old = app.test_client()
    rotated_old.set_cookie(SESSION_COOKIE, first_raw, domain="127.0.0.1")
    captures.append(_capture(app, rotated_old, "old_session_rejection", "get", "/secure/session/profile"))
    captures.append(_capture(app, student, "logout_invalidation", "post", "/secure/session/logout"))

    admin = app.test_client()
    captures.append(_capture(app, admin, "server_session_admin_login", "post", "/login",
        data={"username": "admin_lab", "password": "AdminLab123!", "mode": "session"},
        follow_redirects=False))
    captures.append(_capture(app, admin, "admin_allowed", "get", "/secure/session/admin"))
    return app, captures


def _database_evidence() -> dict[str, Any]:
    connection = connect_database(DATABASE)
    try:
        count_row = connection.execute(
            "SELECT (SELECT COUNT(*) FROM users) AS users, "
            "(SELECT COUNT(*) FROM server_sessions) AS server_sessions, "
            "(SELECT COUNT(*) FROM audit_logs) AS audit_logs, "
            "(SELECT COUNT(*) FROM cookie_events) AS cookie_events, "
            "(SELECT COUNT(*) FROM session_events) AS session_events"
        ).fetchone()
        counts = {name: int(count_row[name]) for name in count_row.keys()}
        audits = [dict(row) for row in connection.execute(
            "SELECT id, timestamp, user_id, username, action, route, mode, cookie_name, "
            "cookie_status, submitted_role, database_role, authorization_decision, reason, trace_id "
            "FROM audit_logs ORDER BY id"
        ).fetchall()]
        cookie_events = [dict(row) for row in connection.execute(
            "SELECT id, timestamp, mode, cookie_name, operation, value_fingerprint, "
            "signature_status, encryption_status, decision, trace_id FROM cookie_events ORDER BY id"
        ).fetchall()]
        session_events = [dict(row) for row in connection.execute(
            "SELECT id, timestamp, user_id, event_type, old_session_fingerprint, "
            "new_session_fingerprint, reason, trace_id FROM session_events ORDER BY id"
        ).fetchall()]
        session_rows = connection.execute(
            "SELECT id, session_token_hash, user_id, created_at, expires_at, last_seen_at, "
            "active, revoked_at, rotation_reason FROM server_sessions ORDER BY id"
        ).fetchall()
        sessions = [
            {
                "id": int(row["id"]),
                "session_hash_fingerprint": fingerprint(str(row["session_token_hash"])),
                "user_id": int(row["user_id"]),
                "created_at": row["created_at"],
                "expires_at": row["expires_at"],
                "last_seen_at": row["last_seen_at"],
                "active": bool(row["active"]),
                "revoked_at": row["revoked_at"],
                "rotation_reason": row["rotation_reason"],
            }
            for row in session_rows
        ]
    finally:
        connection.close()
    return {
        "counts": counts,
        "audit_logs": audits,
        "cookie_events": cookie_events,
        "session_events": session_events,
        "server_sessions": sessions,
    }


def export_evidence() -> dict[str, Any]:
    _app, captures = run_fixed_flows()
    by_name = {capture.name: capture for capture in captures}
    for capture in captures:
        _write_json(EVIDENCE / "traces" / f"{capture.name}.json", capture.trace)
        _write_json(EVIDENCE / "requests" / f"{capture.name}.json", capture.request)
        _write_json(EVIDENCE / "responses" / f"{capture.name}.json", capture.response)
        _write_json(EVIDENCE / "cookies" / f"{capture.name}.json", capture.cookies)

    required_trace_names = {
        "plain_login_student.json": "plain_cookie_login",
        "plain_admin_denied.json": "plain_admin_denied",
        "plain_admin_cookie_modified.json": "plain_cookie_modified",
        "base64_login_student.json": "base64_cookie_login",
        "base64_admin_denied.json": "base64_original",
        "base64_admin_cookie_modified.json": "base64_modified",
        "signed_cookie_valid.json": "signed_cookie_valid",
        "signed_cookie_tampered.json": "signed_cookie_invalid",
        # The encrypted demo performs both real decrypt operations in one fixed request.
        "encrypted_cookie_valid.json": "encrypted_cookie_valid_and_tampered",
        "encrypted_cookie_tampered.json": "encrypted_cookie_valid_and_tampered",
        "server_session_student_login.json": "server_session_student_login",
        "server_session_student_admin_denied.json": "student_admin_denied",
        "server_session_admin_login.json": "server_session_admin_login",
        "server_session_admin_allowed.json": "admin_allowed",
        "server_session_rotated.json": "session_rotation",
        "server_session_logout.json": "logout_invalidation",
        "old_session_rejected.json": "old_session_rejection",
    }
    for required_name, capture_name in required_trace_names.items():
        _write_json(EVIDENCE / "traces" / required_name, by_name[capture_name].trace)

    required_requests = {
        "plain_login_request.txt": "plain_cookie_login",
        "plain_admin_user_cookie_request.txt": "plain_admin_denied",
        "plain_admin_modified_cookie_request.txt": "plain_cookie_modified",
        "base64_admin_user_cookie_request.txt": "base64_original",
        "base64_admin_modified_cookie_request.txt": "base64_modified",
        "signed_valid_request.txt": "signed_cookie_valid",
        "signed_tampered_request.txt": "signed_cookie_invalid",
        "session_student_admin_request.txt": "student_admin_denied",
        "session_admin_request.txt": "admin_allowed",
        "session_logout_request.txt": "logout_invalidation",
    }
    for required_name, capture_name in required_requests.items():
        _write_text(EVIDENCE / "requests" / required_name, by_name[capture_name].request)

    required_responses = {
        "plain_admin_denied_response.txt": "plain_admin_denied",
        "plain_admin_allowed_response.txt": "plain_cookie_modified",
        "base64_admin_denied_response.txt": "base64_original",
        "base64_admin_allowed_response.txt": "base64_modified",
        "signed_valid_response.txt": "signed_cookie_valid",
        "signed_tampered_response.txt": "signed_cookie_invalid",
        "session_student_denied_response.txt": "student_admin_denied",
        "session_admin_allowed_response.txt": "admin_allowed",
        "session_logout_response.txt": "logout_invalidation",
    }
    for required_name, capture_name in required_responses.items():
        _write_text(EVIDENCE / "responses" / required_name, by_name[capture_name].response)

    _write_json(EVIDENCE / "cookies" / "plain_cookie_observation.json", by_name["plain_cookie_login"].cookies)
    _write_json(EVIDENCE / "cookies" / "plain_cookie_diff.json", {
        "original": by_name["plain_admin_denied"].cookies,
        "modified_manually": by_name["plain_cookie_modified"].cookies,
        "decision_before": by_name["plain_admin_denied"].response["decision"],
        "decision_after": by_name["plain_cookie_modified"].response["decision"],
    })
    _write_json(EVIDENCE / "cookies" / "base64_cookie_observation.json", by_name["base64_cookie_login"].cookies)
    _write_json(EVIDENCE / "cookies" / "base64_decoded_original.json", by_name["base64_original"].trace.get("inspectors", {}).get("base64", {}))
    _write_json(EVIDENCE / "cookies" / "base64_decoded_modified.json", by_name["base64_modified"].trace.get("inspectors", {}).get("base64", {}))
    _write_json(EVIDENCE / "cookies" / "signed_cookie_observation.json", by_name["signed_cookie_login"].cookies)
    _write_json(EVIDENCE / "cookies" / "signed_cookie_verification.json", {
        "valid": by_name["signed_cookie_valid"].trace.get("inspectors", {}).get("signature", {}),
        "tampered": by_name["signed_cookie_invalid"].trace.get("inspectors", {}).get("signature", {}),
    })
    _write_json(EVIDENCE / "cookies" / "encrypted_cookie_observation.json", {
        "cookies": by_name["encrypted_cookie_valid_and_tampered"].cookies,
        "inspector": by_name["encrypted_cookie_valid_and_tampered"].trace.get("inspectors", {}).get("encryption", {}),
    })
    _write_json(EVIDENCE / "cookies" / "server_session_cookie_observation.json", by_name["server_session_student_login"].cookies)
    database = _database_evidence()
    _write_json(EVIDENCE / "audit" / "audit_logs.json", database["audit_logs"])
    _write_json(EVIDENCE / "cookies" / "cookie_events.json", database["cookie_events"])
    _write_json(EVIDENCE / "sessions" / "session_events.json", database["session_events"])
    _write_json(EVIDENCE / "sessions" / "server_sessions.json", database["server_sessions"])
    _write_json(EVIDENCE / "sessions" / "session_created.json", {
        "trace": by_name["server_session_student_login"].trace,
        "matching_events": [item for item in database["session_events"] if item["trace_id"] == by_name["server_session_student_login"].trace["trace_id"]],
    })
    _write_json(EVIDENCE / "sessions" / "session_rotated.json", {
        "trace": by_name["session_rotation"].trace,
        "matching_events": [item for item in database["session_events"] if item["trace_id"] == by_name["session_rotation"].trace["trace_id"]],
    })
    _write_json(EVIDENCE / "sessions" / "session_logout_invalidated.json", {
        "trace": by_name["logout_invalidation"].trace,
        "matching_events": [item for item in database["session_events"] if item["trace_id"] == by_name["logout_invalidation"].trace["trace_id"]],
    })
    _write_json(EVIDENCE / "sessions" / "old_session_rejected.json", {
        "trace": by_name["old_session_rejection"].trace,
        "session_status": by_name["old_session_rejection"].response["headers"].get("X-Lab-Session-Status"),
    })
    _write_json(EVIDENCE / "database" / "database_snapshot.json", {
        "database": "Lab06 local SQLite",
        "counts": database["counts"],
        "raw_session_ids_stored": False,
    })
    results = {
        capture.name: {
            "status_code": capture.response["status_code"],
            "decision": capture.response["decision"],
            "trace_id": capture.trace["trace_id"],
        }
        for capture in captures
    }
    _write_json(EVIDENCE / "results" / "flow_results.json", results)
    summary = {
        "generated_at": datetime.now(UTC).isoformat(),
        "flow_count": len(captures),
        "trace_count": len(captures),
        "audit_count": len(database["audit_logs"]),
        "session_event_count": len(database["session_events"]),
        "all_artifacts_redacted": True,
    }
    _write_json(EVIDENCE / "logs" / "evidence_export_summary.json", summary)
    return summary


def main() -> int:
    summary = export_evidence()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
