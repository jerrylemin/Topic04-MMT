from database import query_all, query_one


def _token(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


def test_audit_records_vulnerable_missing_invalid_and_origin_denied_without_secrets(app, logged_in):
    logged_in.post(
        "/vulnerable/change-email",
        data={"email": "audit_attack@lab.local"},
        headers={"Origin": "http://127.0.0.1:9004"},
    )
    logged_in.post(
        "/secure/change-email", data={"email": "missing@lab.local"},
        headers={"Origin": "http://127.0.0.1:5004"},
    )
    logged_in.post(
        "/secure/change-email", data={"email": "invalid@lab.local", "csrf_token": "f" * 43},
        headers={"Origin": "http://127.0.0.1:5004"},
    )
    logged_in.post(
        "/secure/change-email", data={"email": "origin@lab.local", "csrf_token": _token(logged_in)},
        headers={"Origin": "http://127.0.0.1:9004"},
    )
    with app.app_context():
        actions = {row["action"] for row in query_all("SELECT action FROM audit_logs")}
        serialized = " ".join(str(tuple(row)) for row in query_all("SELECT * FROM audit_logs"))
    assert {"vulnerable_email_changed", "csrf_token_missing", "csrf_token_invalid", "origin_denied"} <= actions
    assert "Victim123!" not in serialized
    assert _token(logged_in) not in serialized
    assert "lab04_session=" not in serialized


def test_origin_denial_is_a_real_audit_row(app, logged_in):
    logged_in.post(
        "/secure/change-email",
        data={"email": "blocked@lab.local", "csrf_token": _token(logged_in)},
        headers={"Origin": "http://localhost:9004", "Referer": "http://127.0.0.1:5004/secure/change-email"},
    )
    with app.app_context():
        row = query_one("SELECT * FROM audit_logs WHERE action = 'origin_denied' ORDER BY id DESC")
    assert row["decision"] == "denied"
    assert row["origin"] == "http://localhost:9004"


def test_each_audit_event_links_to_a_saved_trace(app, logged_in):
    with logged_in.session_transaction() as sess:
        token = sess["csrf_token"]
    logged_in.post(
        "/secure/change-email",
        data={"email": "linked_audit@lab.local", "csrf_token": token},
        headers={"Origin": "http://127.0.0.1:5004"},
    )
    with app.app_context():
        missing = query_one(
            """SELECT COUNT(*) AS count FROM audit_logs AS audit
               LEFT JOIN trace_records AS trace ON trace.trace_id = audit.trace_id
               WHERE trace.trace_id IS NULL"""
        )["count"]
    assert missing == 0
