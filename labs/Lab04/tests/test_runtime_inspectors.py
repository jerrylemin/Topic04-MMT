import json

from database import query_one


ORIGIN = {"Origin": "http://127.0.0.1:5004"}


def _token(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


def test_saved_request_inspector_uses_real_request_metadata(app, logged_in):
    logged_in.post(
        "/secure/change-email?source=test",
        data={"email": "inspector@lab.local", "csrf_token": _token(logged_in)},
        headers=ORIGIN,
    )
    with app.app_context():
        payload = json.loads(
            query_one("SELECT payload FROM trace_records ORDER BY created_at DESC LIMIT 1")["payload"]
        )
    assert payload["full_url"].endswith("/secure/change-email?source=test")
    assert payload["path"] == "/secure/change-email"
    assert payload["query_string"] == "source=test"
    assert payload["content_type"].startswith("application/x-www-form-urlencoded")
    assert payload["content_length"] > 0
    assert payload["form_field_names"] == ["csrf_token", "email"]
    assert payload["form_values"]["csrf_token"] == "[REDACTED]"
    assert payload["host"] == "localhost"
    assert payload["route_handler"] == "secure_change_email"


def test_dashboard_cookie_inspector_uses_runtime_host_and_server_masking(logged_in):
    token = _token(logged_in)
    response = logged_in.get("/dashboard", base_url="http://localhost:5004")
    body = response.get_data(as_text=True)
    assert "Observed request host" in body
    assert "localhost:5004" in body
    assert "Runtime config" in body
    assert 'data-token="' not in body
    assert token not in body.split("CSRF Token Inspector", 1)[1]


def test_result_state_inspector_reads_linked_sqlite_history(app, logged_in):
    response = logged_in.post(
        "/secure/change-email",
        data={"email": "state@lab.local", "csrf_token": _token(logged_in)},
        headers=ORIGIN,
    )
    body = response.get_data(as_text=True)
    assert "SQLite state_history" in body
    assert "victim_old@lab.local" in body
    assert "state@lab.local" in body


def test_trace_timeline_renders_all_required_step_fields(logged_in):
    response = logged_in.post(
        "/secure/change-email",
        data={"email": "timeline@lab.local", "csrf_token": _token(logged_in)},
        headers=ORIGIN,
    )
    body = response.get_data(as_text=True)
    for label in ("Timestamp", "Technique", "Input", "Output", "Source file", "Function", "Approx. line"):
        assert label in body


def test_security_controls_are_runtime_records(client):
    body = client.get("/security-controls").get_data(as_text=True)
    for label in ("Runtime status", "Data source", "Config/source file", "Applied routes", "Risk reduced", "Limitation"):
        assert label in body
    assert "MAX_CONTENT_LENGTH" in body


def test_code_comparison_is_extracted_from_real_source(client):
    body = client.get("/comparison").get_data(as_text=True)
    assert "victim_app.py" in body
    assert "secure_change_email" in body
    assert "Line start" in body and "Line end" in body
    assert "def secure_change_email" in body
