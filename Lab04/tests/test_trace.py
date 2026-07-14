import json

from database import query_one


def test_trace_records_observed_request_and_redacted_state(app, logged_in):
    response = logged_in.post(
        "/vulnerable/change-email",
        data={"email": "trace@lab.local"},
        headers={"Origin": "http://127.0.0.1:9004", "Referer": "http://127.0.0.1:9004/attack/vulnerable-email"},
    )
    assert response.status_code == 200
    with app.app_context():
        payload = json.loads(query_one("SELECT payload FROM trace_records ORDER BY created_at DESC LIMIT 1")["payload"])
    assert payload["cookie_present"] is True
    assert payload["origin"] == "http://127.0.0.1:9004"
    assert payload["referer"] == "http://127.0.0.1:9004/attack/vulnerable-email"
    assert "csrf_token_status" in payload
    assert "state_before" in payload and "state_after" in payload
    assert [step["step_number"] for step in payload["steps"]] == list(range(1, 17))
    assert {step["layer"] for step in payload["steps"]} >= {
        "Victim Browser", "Cookie Policy", "HTTP Request", "Flask Router", "Authentication",
        "Origin Validation", "CSRF Validation", "Re-authentication", "Input Validation",
        "SQLite", "HTTP Response", "Same-Origin Policy", "Final Result",
    }
    serialized = json.dumps(payload)
    assert "Victim123!" not in serialized


def test_trace_api_returns_real_saved_trace(app, logged_in):
    logged_in.post("/vulnerable/change-email", data={"email": "trace@lab.local"})
    with app.app_context():
        trace_id = query_one("SELECT trace_id FROM trace_records ORDER BY created_at DESC LIMIT 1")["trace_id"]
    response = logged_in.get(f"/api/trace/{trace_id}")
    assert response.status_code == 200
    assert response.get_json()["trace_id"] == trace_id
    assert response.get_json()["request_sent"] is True
    assert "response_readable_by_attacker" in response.get_json()


def test_state_history_and_saved_trace_share_trace_id(app, logged_in):
    logged_in.post("/vulnerable/change-email", data={"email": "linked@lab.local"})
    with app.app_context():
        history = query_one("SELECT trace_id FROM state_history ORDER BY id DESC LIMIT 1")["trace_id"]
        trace = query_one("SELECT trace_id FROM trace_records WHERE trace_id = ?", (history,))
    assert trace is not None


def test_read_only_request_also_creates_a_real_trace(app, client):
    client.get("/health")
    with app.app_context():
        trace = query_one("SELECT payload FROM trace_records ORDER BY created_at DESC LIMIT 1")
    payload = json.loads(trace["payload"])
    assert payload["action"] == "request_observed"
    assert payload["request_method"] == "GET"
    assert len(payload["steps"]) == 16
