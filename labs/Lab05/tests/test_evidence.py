import json
import re

import pytest

from scripts import export_evidence as exporter


def test_fixed_flow_runner_captures_all_required_real_flows(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter.Config, "DATABASE", str(tmp_path / "flows.sqlite3"))
    captured, state = exporter.run_fixed_flows()
    assert set(captured) == set(exporter.TRACE_NAMES)
    assert len(captured) == 12
    assert len(state["query_events"]) == 12
    assert state["counts"]["users"] == 3
    assert state["counts"]["products"] >= 8


def test_evidence_export_writes_trace_request_response_query_and_audit(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter, "ROOT", tmp_path)
    monkeypatch.setattr(exporter.Config, "DATABASE", str(tmp_path / "evidence.sqlite3"))
    summary = exporter.export_evidence()
    assert summary["flows"] == 12
    assert len(list((tmp_path / "evidence" / "traces").glob("*.json"))) == 12
    assert len(list((tmp_path / "evidence" / "requests").glob("*.txt"))) == 10
    assert len(list((tmp_path / "evidence" / "responses").glob("*.txt"))) == 10
    assert len(list((tmp_path / "evidence" / "queries").glob("*.json"))) == 4
    assert (tmp_path / "evidence" / "audit" / "audit_logs.json").is_file()


def test_exported_trace_json_is_linked_to_real_request(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter, "ROOT", tmp_path)
    monkeypatch.setattr(exporter.Config, "DATABASE", str(tmp_path / "linked.sqlite3"))
    exporter.export_evidence()
    trace = json.loads((tmp_path / "evidence" / "traces" / "normal_search_secure.json").read_text(encoding="utf-8"))
    assert trace["request_inspector"]["path"] == "/secure/search"
    assert trace["query_inspector"]["prepared"] is True
    assert trace["steps"]


@pytest.mark.parametrize("secret", ["AdminLab123!", "StudentA123!", "a" * 64])
def test_redaction_guard_rejects_plaintext_password_or_full_digest(secret):
    with pytest.raises(RuntimeError, match="Evidence contains"):
        exporter._assert_redacted({"value": secret})


def test_request_evidence_redacts_password_value(shared_client):
    response = shared_client.post(
        "/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"}
    )
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    evidence = exporter._request_text(trace)
    assert "[REDACTED]" in evidence
    assert "AdminLab123!" not in evidence
    assert "Timestamp:" in evidence


def test_response_evidence_contains_decision_not_full_html(shared_client):
    response = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    evidence = exporter._response_text(response, trace)
    assert "Decision: expected_results" in evidence
    assert "Trace ID:" in evidence
    assert "<html" not in evidence.lower()


def test_evidence_values_have_no_full_hex_digest(monkeypatch, tmp_path):
    monkeypatch.setattr(exporter.Config, "DATABASE", str(tmp_path / "redacted.sqlite3"))
    captured, state = exporter.run_fixed_flows()
    serialized = json.dumps({name: trace for name, (_, trace) in captured.items()}) + json.dumps(state)
    assert not re.search(r"\b[a-f0-9]{64}\b", serialized, re.IGNORECASE)

