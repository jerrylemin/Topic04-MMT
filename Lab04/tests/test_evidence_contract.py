import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TRACE_FILES = [
    "login_victim.json", "vulnerable_email_change.json", "secure_email_missing_token.json",
    "secure_email_invalid_token.json", "secure_email_origin_denied.json", "secure_email_success.json",
    "logout_csrf_denied.json", "logout_success.json", "reset_csrf_denied.json", "reset_success.json",
]
REDIRECT_TRACE_FILES = {"login_victim.json", "logout_success.json", "reset_success.json"}
REQUEST_FILES = [
    "login_request.txt", "vulnerable_email_request.txt", "secure_missing_token_request.txt",
    "secure_invalid_token_request.txt", "secure_valid_request.txt", "logout_request.txt", "reset_request.txt",
]
RESPONSE_FILES = [name.replace("request", "response") for name in REQUEST_FILES]


@pytest.mark.parametrize("filename", TRACE_FILES)
def test_named_trace_evidence_is_real_complete_and_redacted(filename):
    trace = json.loads((ROOT / "evidence/traces" / filename).read_text(encoding="utf-8"))
    assert trace["trace_id"] and len(trace["steps"]) == 16
    assert trace["request_method"] in {"GET", "POST"}
    for step in trace["steps"]:
        assert step["technique"]
        assert step["input_data"]
        assert step["output_data"]
        assert step["code_reference"]
        assert step["security_meaning"]
        assert step["status"]
    serialized = json.dumps(trace)
    assert "Victim123!" not in serialized
    assert "password_hash" not in serialized
    assert "lab04_session=" not in serialized
    if filename in REDIRECT_TRACE_FILES:
        assert trace["http_status"] == 303


@pytest.mark.parametrize("filename", REQUEST_FILES)
def test_named_request_evidence_contains_observed_metadata_without_secrets(filename):
    text = (ROOT / "evidence/requests" / filename).read_text(encoding="utf-8")
    for label in ("Method:", "URL:", "Path:", "Host:", "Cookie present:", "CSRF status:", "Timestamp:"):
        assert label in text
    assert "Victim123!" not in text and "lab04_session=" not in text


@pytest.mark.parametrize("filename", RESPONSE_FILES)
def test_named_response_evidence_contains_real_decision(filename):
    text = (ROOT / "evidence/responses" / filename).read_text(encoding="utf-8")
    for label in ("HTTP status:", "Content-Type:", "Trace ID:", "Decision:", "CSRF status:", "Origin decision:"):
        assert label in text


@pytest.mark.parametrize("relative", [
    "evidence/audit/audit_logs.json",
    "evidence/state/state_transitions.json",
    "evidence/logs/baseline_review.txt",
    "evidence/logs/runtime_smoke_test.txt",
])
def test_supporting_evidence_is_nonempty(relative):
    path = ROOT / relative
    assert path.exists() and path.stat().st_size > 20
