import json

from flask import request

from database import execute, query_all
from security_utils import redact


def log_event(*, action: str, mode: str, username_submitted: str | None,
              input_summary: dict, query: dict, decision: str, reason: str,
              result_count: int, error_category: str | None, trace_id: str) -> None:
    execute(
        """INSERT INTO audit_logs
           (action, route, mode, username_submitted, input_summary, query_template,
            parameter_count, decision, reason, result_count, error_category, trace_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            action, request.path, mode, username_submitted,
            json.dumps(redact(input_summary), ensure_ascii=False), query.get("query_template"),
            query.get("placeholder_count", 0), decision, reason, result_count, error_category, trace_id,
        ),
    )


def log_login_attempt(*, mode: str, username: str, success: bool,
                      user_id: int | None, reason: str, trace_id: str) -> None:
    execute(
        """INSERT INTO login_attempts
           (mode, username_submitted, success, matched_user_id, reason, trace_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (mode, username, int(success), user_id, reason, trace_id),
    )


def log_query_event(*, mode: str, feature: str, query: dict, result_count: int,
                    error_category: str | None, trace_id: str) -> None:
    execute(
        """INSERT INTO query_events
           (mode, feature, query_template, final_query_masked, parameters_json,
            result_count, error_category, trace_id)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            mode, feature, query["query_template"], query["final_query_masked"],
            json.dumps(redact(query.get("parameters_masked", [])), ensure_ascii=False),
            result_count, error_category, trace_id,
        ),
    )


def list_logs(limit: int = 200):
    return query_all("SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?", (limit,))

