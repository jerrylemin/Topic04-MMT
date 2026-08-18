import json
import uuid

from flask import request, session
from werkzeug.exceptions import HTTPException

from database import execute, query_one
from origin_service import ALLOWED_ORIGINS, parse_origin
from security_utils import redact
from trace_models import RequestTrace


def new_trace_id() -> str:
    return uuid.uuid4().hex


def request_trace(mode: str, action: str, *, csrf_status: str = "not_required",
                  origin_decision: str = "not_checked", state_before=None, state_after=None,
                  status: int = 200, result: str = "request_received",
                  reauth_status: str = "not_required", steps=None, trace_id: str | None = None) -> dict:
    origin = request.headers.get("Origin")
    referer = request.headers.get("Referer")
    parsed_origin = parse_origin(origin)
    parsed_referer = parse_origin(referer, allow_path=True)
    inspected = parsed_origin or parsed_referer
    victim = parse_origin(request.host_url, allow_path=True)
    victim_origin = victim["origin"] if victim else request.host_url.rstrip("/")
    try:
        form_values = redact(request.form.to_dict())
        csrf_present = bool(request.form.get("csrf_token"))
    except HTTPException:
        form_values = {}
        csrf_present = False
    trace = RequestTrace(
        trace_id=trace_id or new_trace_id(),
        mode=mode,
        action=action,
        current_user=session.get("username"),
        attacker_origin=origin,
        victim_origin=victim_origin,
        same_origin=bool(parsed_origin and parsed_origin["origin"] == victim_origin) if origin else None,
        same_site=bool(parsed_origin and victim and parsed_origin["scheme"] == victim["scheme"] and
                       parsed_origin["hostname"] == victim["hostname"]) if origin else None,
        request_method=request.method,
        full_url=request.url,
        path=request.path,
        query_string=request.query_string.decode("utf-8", errors="replace"),
        content_type=request.content_type,
        content_length=request.content_length or 0,
        form_field_names=sorted(form_values),
        form_values=form_values,
        host=request.host,
        route_handler=request.endpoint or "",
        cookie_present=bool(request.cookies.get("lab04_session")),
        origin_header=origin,
        referer_header=referer,
        parsed_scheme=inspected["scheme"] if inspected else None,
        parsed_hostname=inspected["hostname"] if inspected else None,
        parsed_port=inspected["port"] if inspected else None,
        expected_origins=sorted(ALLOWED_ORIGINS),
        origin_match=bool(parsed_origin and parsed_origin["origin"] in ALLOWED_ORIGINS) if origin else None,
        referer_match=bool(parsed_referer and parsed_referer["origin"] in ALLOWED_ORIGINS) if referer else None,
        csrf_token_present=csrf_present,
        csrf_token_status=csrf_status,
        origin_decision=origin_decision,
        reauthentication_status=reauth_status,
        state_before=redact(state_before or {}),
        state_after=redact(state_after or {}),
        http_status=status,
        final_result=result,
        response_readable_by_attacker=False if parsed_origin and parsed_origin["origin"] != victim_origin else True,
        steps=steps or [],
    )
    return trace.to_dict()
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
