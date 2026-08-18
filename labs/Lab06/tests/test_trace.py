from __future__ import annotations

import json
from datetime import UTC, datetime

from trace_models import FinalVerdict
from trace_service import TraceStore, add_step, begin_trace, clear_traces, export_trace, finish_trace, get_trace


def _verdict():
    return FinalVerdict(
        mode="plain", cookie_name="lab06_role", cookie_source="client",
        role_source="cookie", integrity_protected=False,
        confidentiality_protected=False, server_session_used=False,
        cookie_modified=False, modification_detected=False,
        database_role_checked=False, authorization_decision="deny",
        access_granted=False, audit_event="plain_admin_denied",
        root_cause="client-controlled role", primary_fix="database authorization",
        defense_in_depth="cookie flags", remaining_risk="manual cookie editing",
    )


def test_begin_trace_generates_prefixed_identifier():
    trace = begin_trace(mode="plain", route="/vulnerable/plain/admin")
    assert trace.trace_id.startswith("trace_") and len(trace.trace_id) == 30
    assert get_trace(trace.trace_id) is trace


def test_add_step_assigns_order_and_required_fields():
    trace = begin_trace(mode="plain", route="/vulnerable/plain/admin")
    first = add_step(
        trace, layer="HTTP Request", title="Request", description="Observed",
        technique="request.cookies", input_data={"role": "user"},
        output_data={"decision": "deny"}, code_reference="app.py:plain_admin",
        security_meaning="Client-controlled", status="observed",
    )
    second = add_step(
        trace, layer="Authorization", title="Decision", description="Denied",
        technique="role comparison", input_data={}, output_data={},
        code_reference="authorization_service.py", security_meaning="Policy", status="deny",
    )
    assert (first.step_number, second.step_number) == (1, 2)
    assert first.technique and first.code_reference and first.security_meaning


def test_trace_redacts_sensitive_nested_values():
    trace = begin_trace(mode="session", route="/secure/session/profile")
    step = add_step(
        trace, layer="Session", title="Lookup", description="Hash lookup",
        technique="SHA-256", input_data={"raw_token": "must-not-appear"},
        output_data={"password_hash": "must-not-appear"}, code_reference="session_resolution",
        security_meaning="Opaque token", status="valid",
    )
    serialized = json.dumps(step.to_dict())
    assert "must-not-appear" not in serialized and "[REDACTED]" in serialized


def test_finish_trace_attaches_real_verdict():
    trace = begin_trace(mode="plain", route="/vulnerable/plain/admin")
    finish_trace(trace, status="completed", verdict=_verdict())
    assert trace.status == "completed" and trace.completed_at
    assert trace.verdict.authorization_decision == "deny"


def test_trace_export_serializes_completed_trace(tmp_path):
    trace = begin_trace(mode="plain", route="/vulnerable/plain/admin", now=datetime(2026, 1, 1, tzinfo=UTC))
    finish_trace(trace, status="completed", verdict=_verdict(), now=datetime(2026, 1, 1, 0, 0, 1, tzinfo=UTC))
    path = export_trace(trace, tmp_path / "trace.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["trace_id"] == trace.trace_id and payload["verdict"]["access_granted"] is False


def test_trace_store_evicts_oldest_entry():
    store = TraceStore(max_items=1)
    first = begin_trace(mode="plain", route="/one")
    second = begin_trace(mode="plain", route="/two")
    store.put(first)
    store.put(second)
    assert store.get(first.trace_id) is None and store.get(second.trace_id) is second


def test_clear_traces_returns_removed_count():
    clear_traces()
    begin_trace(mode="plain", route="/one")
    begin_trace(mode="base64", route="/two")
    assert clear_traces() == 2


def test_trace_api_rejects_unknown_identifier(client):
    assert client.get("/api/trace/not-present").status_code == 404


def test_runtime_trace_uses_mode_specific_security_technique(client):
    client.post(
        "/login",
        data={"username": "admin_lab", "password": "AdminLab123!", "mode": "signed"},
    )
    response = client.get("/secure/signed/admin")
    trace = client.get(f"/api/trace/{response.headers['X-Lab-Trace-ID']}").get_json()

    security_step = trace["steps"][1]
    assert "signature verification" in security_step["technique"]
    assert security_step["code_reference"] == "signed_cookie_service.py:verify_signed_profile"
    assert "client role comparison" not in security_step["technique"]
