import json

from config import AUTH_LOGIC_INPUT, QUOTE_INPUT, SEARCH_EXPANDED_INPUT
from database import query_all, query_one


def _actions(app):
    with app.app_context():
        return [row["action"] for row in query_all("SELECT action FROM audit_logs ORDER BY id")]


def test_normal_secure_login_records_success_event(shared_app, shared_client, clear_events):
    shared_client.post("/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    assert _actions(shared_app) == ["secure_login_success"]


def test_quote_login_records_detection_error_and_handling(shared_app, shared_client, clear_events):
    shared_client.post("/vulnerable/login", data={"username": QUOTE_INPUT, "password": "x"})
    assert _actions(shared_app) == ["login_quote_detected", "login_query_error", "database_error_handled"]


def test_local_bypass_records_logic_change_and_demo_event(shared_app, shared_client, clear_events):
    shared_client.post("/vulnerable/login", data={"username": AUTH_LOGIC_INPUT, "password": "wrong"})
    assert _actions(shared_app) == ["login_logic_changed", "login_bypass_local_demo"]


def test_expanded_search_records_condition_and_unexpected_result(shared_app, shared_client, clear_events):
    shared_client.get("/vulnerable/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    assert _actions(shared_app) == ["search_condition_changed", "search_unexpected_result"]


def test_validation_failure_is_audited(shared_app, shared_client, clear_events):
    shared_client.get("/secure/user", query_string={"id": "bad"})
    assert _actions(shared_app) == ["validation_failed"]


def test_audit_row_links_route_decision_and_trace(shared_app, shared_client, clear_events):
    response = shared_client.get("/secure/search", query_string={"keyword": "USB"})
    with shared_app.app_context():
        row = dict(query_one("SELECT * FROM audit_logs"))
    assert row["route"] == "/secure/search"
    assert row["decision"] == "expected_results"
    assert row["trace_id"] == response.headers["X-Lab-Trace-ID"]
    assert row["parameter_count"] == 1


def test_audit_and_query_events_never_store_password_or_hash(shared_app, shared_client, clear_events):
    shared_client.post("/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    with shared_app.app_context():
        audit = [dict(row) for row in query_all("SELECT * FROM audit_logs")]
        queries = [dict(row) for row in query_all("SELECT * FROM query_events")]
    serialized = json.dumps({"audit": audit, "queries": queries})
    assert "AdminLab123!" not in serialized
    assert "pbkdf2:sha256:600000" not in serialized


def test_audit_page_renders_recorded_event(shared_client, clear_events):
    shared_client.get("/secure/search", query_string={"keyword": "USB"})
    response = shared_client.get("/audit-logs")
    assert response.status_code == 200
    assert b"secure_search_completed" in response.data

