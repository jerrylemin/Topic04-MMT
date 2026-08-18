from flask import request, session

from database import get_db, query_all
from security_utils import safe_value


def log_event(action: str, mode: str, decision: str, reason: str, trace_id: str,
              parameter_name: str = "", original_value=None, submitted_value=None) -> None:
    db = get_db()
    db.execute(
        """INSERT INTO audit_logs
           (user_id, username, action, route, mode, parameter_name, original_value,
            submitted_value, decision, reason, ip_address, trace_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (session.get("user_id"), session.get("username"), action, request.path, mode,
         parameter_name, safe_value(parameter_name, original_value), safe_value(parameter_name, submitted_value),
         decision, reason, request.remote_addr or "127.0.0.1", trace_id),
    )
    db.commit()


def list_logs(user_id=None, action: str = "", mode: str = "", decision: str = "", trace_id: str = "") -> list[dict]:
    rows = query_all(
        """SELECT * FROM audit_logs
           WHERE (? IS NULL OR user_id = ?)
             AND (? = '' OR action = ?)
             AND (? = '' OR mode = ?)
             AND (? = '' OR decision = ?)
             AND (? = '' OR trace_id = ?)
           ORDER BY id DESC LIMIT 200""",
        (user_id, user_id, action, action, mode, mode, decision, decision, trace_id, trace_id),
    )
    return [dict(row) for row in rows]

