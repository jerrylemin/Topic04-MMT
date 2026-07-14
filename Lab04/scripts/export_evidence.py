"""Generate named evidence from the real Flask handlers and SQLite database."""

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from config import Config  # noqa: E402
from database import query_one  # noqa: E402
from seed import reset_database  # noqa: E402
from victim_app import create_app  # noqa: E402


ORIGIN = {"Origin": "http://127.0.0.1:5004"}


def _json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def _text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def _token(client) -> str:
    with client.session_transaction() as session:
        return session["csrf_token"]


def _latest_trace(app, action: str) -> dict:
    with app.app_context():
        row = query_one(
            "SELECT payload FROM trace_records WHERE json_extract(payload, '$.action') = ? ORDER BY created_at DESC LIMIT 1",
            (action,),
        )
    if not row:
        raise RuntimeError(f"No saved trace for action {action!r}.")
    return json.loads(row["payload"])


def _request_text(trace: dict) -> str:
    return "\n".join((
        f"Method: {trace['request_method']}",
        f"URL: {trace['full_url']}",
        f"Path: {trace['path']}",
        f"Query: {trace['query_string'] or '-'}",
        f"Content-Type: {trace['content_type'] or '-'}",
        f"Content-Length: {trace['content_length']}",
        f"Origin: {trace['origin_header'] or '-'}",
        f"Referer: {trace['referer_header'] or '-'}",
        f"Host: {trace['host']}",
        f"Cookie present: {trace['cookie_present']}",
        f"Session user: {trace['current_user'] or '-'}",
        f"CSRF status: {trace['csrf_token_status']}",
        f"Form: {json.dumps(trace['form_values'], ensure_ascii=False)}",
        f"Timestamp: {trace['timestamp']}",
    )) + "\n"


def _response_text(response, trace: dict) -> str:
    return "\n".join((
        f"HTTP status: {response.status_code}",
        f"Location: {response.headers.get('Location', '-')}",
        f"Content-Type: {response.headers.get('Content-Type', '-')}",
        f"Content-Length: {response.headers.get('Content-Length', '-')}",
        f"Trace ID: {trace['trace_id']}",
        f"Decision: {trace['final_result']}",
        f"CSRF status: {trace['csrf_token_status']}",
        f"Origin decision: {trace['origin_decision']}",
    )) + "\n"


def main() -> int:
    app = create_app({"TESTING": True, "DATABASE": Config.DATABASE, "SERVER_NAME": "127.0.0.1:5004"})
    with app.app_context():
        reset_database()
    client = app.test_client()
    captured = {}

    def run(name, action, method, path, **kwargs):
        response = getattr(client, method)(path, **kwargs)
        captured[name] = (response, _latest_trace(app, action))

    run("login_victim", "login_success", "post", "/login", data={"username": "victim", "password": "Victim123!"})
    run("vulnerable_email_change", "vulnerable_email_changed", "post", "/vulnerable/change-email",
        data={"email": "demo_changed@lab.local"}, headers={"Origin": "http://127.0.0.1:9004"})
    run("secure_email_missing_token", "csrf_token_missing", "post", "/secure/change-email",
        data={"email": "missing@lab.local"}, headers=ORIGIN)
    run("secure_email_invalid_token", "csrf_token_invalid", "post", "/secure/change-email",
        data={"email": "invalid@lab.local", "csrf_token": "x" * 43}, headers=ORIGIN)
    run("secure_email_origin_denied", "origin_denied", "post", "/secure/change-email",
        data={"email": "origin@lab.local", "csrf_token": _token(client)}, headers={"Origin": "http://127.0.0.1:9004"})
    run("secure_email_success", "secure_email_changed", "post", "/secure/change-email",
        data={"email": "secure_success@lab.local", "csrf_token": _token(client)}, headers=ORIGIN)
    run("logout_csrf_denied", "logout_csrf_denied", "post", "/logout", headers=ORIGIN)
    run("logout_success", "logout_success", "post", "/logout",
        data={"csrf_token": _token(client)}, headers=ORIGIN)
    client.post("/login", data={"username": "victim", "password": "Victim123!"})
    run("reset_csrf_denied", "lab_reset_csrf_denied", "post", "/reset-lab", headers=ORIGIN)
    run("reset_success", "lab_reset", "post", "/reset-lab",
        data={"csrf_token": _token(client)}, headers=ORIGIN)

    for name, (_response, trace) in captured.items():
        _json(ROOT / f"evidence/traces/{name}.json", trace)

    request_map = {
        "login_request.txt": "login_victim",
        "vulnerable_email_request.txt": "vulnerable_email_change",
        "secure_missing_token_request.txt": "secure_email_missing_token",
        "secure_invalid_token_request.txt": "secure_email_invalid_token",
        "secure_valid_request.txt": "secure_email_success",
        "logout_request.txt": "logout_success",
        "reset_request.txt": "reset_success",
    }
    response_map = {name.replace("request", "response"): flow for name, flow in request_map.items()}
    for filename, flow in request_map.items():
        _text(ROOT / "evidence/requests" / filename, _request_text(captured[flow][1]))
    for filename, flow in response_map.items():
        _text(ROOT / "evidence/responses" / filename, _response_text(*captured[flow]))

    database = sqlite3.connect(Config.DATABASE)
    database.row_factory = sqlite3.Row
    audits = [dict(row) for row in database.execute("SELECT * FROM audit_logs ORDER BY id")]
    states = [dict(row) for row in database.execute("SELECT * FROM state_history ORDER BY id")]
    database.close()
    _json(ROOT / "evidence/audit/audit_logs.json", audits)
    _json(ROOT / "evidence/state/state_transitions.json", states)
    print(f"Exported {len(captured)} named traces, {len(audits)} audit rows, and {len(states)} state rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
