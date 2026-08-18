import json
from uuid import uuid4

from flask import request, session

from database import get_db, query_one
from security_utils import mask_cookie, safe_mapping
from trace_models import Trace, TraceStep


def new_trace(scenario: str, mode: str) -> Trace:
    return Trace(
        trace_id=uuid4().hex,
        scenario=scenario,
        mode=mode,
        current_user={"user_id": session.get("user_id"), "username": session.get("username"), "role": session.get("role")},
        request_inspector={
            "method": request.method, "url": request.url, "path": request.path,
            "query_string": request.query_string.decode("utf-8", "replace"),
            "content_type": request.content_type or "", "form_body": safe_mapping(request.form),
            "parameters": safe_mapping(request.values), "cookie": mask_cookie(request.headers.get("Cookie", "")),
            "route_handler": request.endpoint, "session": {
                "authenticated_user_id": session.get("user_id"), "username": session.get("username"),
                "role": session.get("role"), "source": "Flask signed session", "cookie": "session=***",
            },
        },
    )


def step(trace: Trace, layer: str, title: str, description: str, *, technique: str = "",
         input_data="", output_data="", code_reference: str = "", security_meaning: str = "",
         status: str = "normal") -> None:
    trace.steps.append(TraceStep(len(trace.steps) + 1, layer, title, description, technique,
                                 input_data, output_data, code_reference, security_meaning, status))


def save_trace(trace: Trace) -> dict:
    payload = trace.to_dict()
    db = get_db()
    db.execute(
        "INSERT OR REPLACE INTO trace_records(trace_id, payload_json) VALUES (?, ?)",
        (trace.trace_id, json.dumps(payload, ensure_ascii=False)),
    )
    db.commit()
    return payload


def get_trace(trace_id: str) -> dict | None:
    row = query_one("SELECT payload_json FROM trace_records WHERE trace_id = ?", (trace_id,))
    return json.loads(row["payload_json"]) if row else None


def clear_traces() -> None:
    db = get_db()
    db.execute("DELETE FROM trace_records")
    db.commit()

