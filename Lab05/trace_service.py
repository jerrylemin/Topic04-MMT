import json
import uuid

from flask import request, session

from database import execute, query_one
from query_trace import inspectors, timeline
from security_utils import redact
from trace_models import RequestTrace, utc_now


def new_trace_id() -> str:
    return uuid.uuid4().hex


def build_trace(*, mode: str, feature: str, raw_input: str, normalized_input: str,
                query: dict, rows: list, error_info: dict | None, decision: str,
                expected_count: int | None = None, session_created: bool = False,
                trace_id: str | None = None) -> dict:
    trace_id = trace_id or new_trace_id()
    request_inspector = {
        "timestamp": utc_now(),
        "method": request.method, "full_url": request.url, "path": request.path,
        "query_string": request.query_string.decode("utf-8", errors="replace"),
        "content_type": request.content_type, "content_length": request.content_length or 0,
        "form_field_names": sorted(request.form.keys()),
        "form_values": {key: ("[REDACTED]" if key.lower() == "password" else value)
                        for key, value in request.form.items()},
        "session_present": bool(session.get("user_id")), "route_handler": request.endpoint,
    }
    panels = inspectors(
        feature=feature, mode=mode, raw_input=raw_input, normalized_input=normalized_input,
        query=query, rows=rows, error_info=error_info, decision=decision,
        expected_count=expected_count, session_created=session_created,
    )
    verdict = {
        "feature": feature, "mode": mode,
        "input_category": "fixed_test" if any(("'" in raw_input, "--" in raw_input)) else "normal",
        "query_construction": query.get("construction_method"),
        "sql_structure_changed": mode == "vulnerable" and decision in {"local_demo_bypass", "unexpected_results"},
        "prepared_statement_used": bool(query.get("prepared")),
        "authentication_bypassed": decision == "local_demo_bypass",
        "unexpected_rows_returned": decision == "unexpected_results",
        "database_error_occurred": bool(error_info), "database_modified": False,
        "sensitive_data_exposed": False, "session_created": session_created,
        "root_cause": "SQL string concatenation" if mode == "vulnerable" else "none observed",
        "primary_fix": "Parameterized query and PBKDF2 verification",
        "remaining_risk": "Local educational demonstration only",
    }
    trace = RequestTrace(
        trace_id=trace_id, mode=mode, feature=feature, request_inspector=request_inspector,
        input_inspector=panels["input_inspector"], query_inspector=panels["query_inspector"],
        execution_inspector=panels["execution_inspector"], decision_inspector=panels["decision_inspector"],
        database_inspector=panels["database_inspector"], error_inspector=error_info,
        final_verdict=verdict,
        steps=timeline(feature=feature, mode=mode, raw_input=raw_input, query=query,
                       rows=rows, decision=decision, error_info=error_info),
    ).to_dict()
    trace["result_set_inspector"] = panels["result_set_inspector"]
    return redact(trace)


def save_trace(trace: dict) -> dict:
    clean = redact(trace)
    execute(
        "INSERT OR REPLACE INTO trace_records (trace_id, payload) VALUES (?, ?)",
        (clean["trace_id"], json.dumps(clean, ensure_ascii=False)),
    )
    return clean


def get_trace(trace_id: str):
    row = query_one("SELECT payload FROM trace_records WHERE trace_id = ?", (trace_id,))
    return json.loads(row["payload"]) if row else None


def clear_traces() -> None:
    execute("DELETE FROM trace_records")
