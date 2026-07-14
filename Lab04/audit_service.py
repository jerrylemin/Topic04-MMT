import json

from flask import request, session

from database import execute, query_all
from security_utils import redact
from trace_service import new_trace_id


def log_event(action: str, *, mode: str, decision: str, reason: str,
              csrf_status: str = "not_required", state_before=None, state_after=None,
              trace_id: str | None = None) -> str:
    trace_id = trace_id or new_trace_id()
    before = json.dumps(redact(state_before or {}), ensure_ascii=False)
    after = json.dumps(redact(state_after or {}), ensure_ascii=False)
    execute(
        """INSERT INTO audit_logs
           (user_id, username, action, route, mode, origin, referer,
            csrf_token_status, cookie_present, decision, reason,
            state_before, state_after, trace_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session.get("user_id"), session.get("username"), action, request.path, mode,
            request.headers.get("Origin"), request.headers.get("Referer"), csrf_status,
            int(bool(request.cookies.get("lab04_session"))), decision, reason,
            before, after, trace_id,
        ),
    )
    return trace_id


def list_logs(user_id=None, action: str = "", mode: str = "", decision: str = "", trace_id: str = "", username: str = ""):
    clauses, parameters = [], []
    for column, value in (("user_id", user_id), ("action", action), ("mode", mode),
                          ("decision", decision), ("trace_id", trace_id), ("username", username)):
        if value not in (None, ""):
            clauses.append(f"{column} = ?")
            parameters.append(value)
    where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
    return query_all(f"SELECT * FROM audit_logs{where} ORDER BY id DESC LIMIT 200", tuple(parameters))
