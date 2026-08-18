import pytest

from database import query_all, query_one


ORIGIN = {"Origin": "http://127.0.0.1:5004"}


def _token(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


@pytest.mark.parametrize(
    ("route", "event"),
    (("/logout", "logout_csrf_denied"), ("/reset-lab", "lab_reset_csrf_denied")),
)
def test_protected_session_routes_log_required_denial_event(app, logged_in, route, event):
    assert logged_in.post(route, headers=ORIGIN).status_code == 403
    with app.app_context():
        row = query_one("SELECT * FROM audit_logs WHERE action = ? ORDER BY id DESC", (event,))
        trace = query_one("SELECT trace_id FROM trace_records WHERE trace_id = ?", (row["trace_id"],))
    assert row["decision"] == "denied"
    assert trace is not None


def test_logout_success_logs_required_event(app, logged_in):
    assert logged_in.post("/logout", data={"csrf_token": _token(logged_in)}, headers=ORIGIN).status_code == 303
    with app.app_context():
        assert query_one("SELECT action FROM audit_logs WHERE action = 'logout_success'") is not None


def test_reset_success_preserves_audit_trace_and_state(app, logged_in):
    assert logged_in.post("/reset-lab", data={"csrf_token": _token(logged_in)}, headers=ORIGIN).status_code == 303
    with app.app_context():
        audit = query_one("SELECT * FROM audit_logs WHERE action = 'lab_reset' ORDER BY id DESC")
        trace = query_one("SELECT trace_id FROM trace_records WHERE trace_id = ?", (audit["trace_id"],))
        state = query_one("SELECT trace_id FROM state_history WHERE trace_id = ?", (audit["trace_id"],))
    assert trace is not None and state is not None


def test_referer_success_is_logged_as_referer_allowed(app, logged_in):
    response = logged_in.post(
        "/secure/change-email",
        data={"email": "referer@lab.local", "csrf_token": _token(logged_in)},
        headers={"Referer": "http://127.0.0.1:5004/secure/change-email"},
    )
    assert response.status_code == 200
    with app.app_context():
        actions = {row["action"] for row in query_all("SELECT action FROM audit_logs")}
    assert "referer_allowed" in actions


def test_audit_page_filters_by_username(app, logged_in):
    response = logged_in.get("/audit-logs?username=victim")
    assert response.status_code == 200
    assert b'Username' in response.data
