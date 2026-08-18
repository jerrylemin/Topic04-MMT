from __future__ import annotations

import json

import pytest

from audit_service import AuditEvent, export_audit_events, list_audit_events, record_audit
from database import connect_database
from seed import seed_database


@pytest.fixture()
def connection(tmp_path):
    conn = connect_database(seed_database(tmp_path / "audit.sqlite3"))
    yield conn
    conn.close()


def _event(**overrides):
    values = dict(
        action="plain_admin_denied", route="/vulnerable/plain/admin", mode="plain",
        reason="client_cookie_role_not_admin", trace_id="trace_0123456789abcdef01234567",
        user_id=10, username="student", cookie_name="lab06_role",
        cookie_status="present", submitted_role="user", database_role=None,
        authorization_decision="deny",
    )
    values.update(overrides)
    return AuditEvent(**values)


def test_record_and_list_audit_event(connection):
    event_id = record_audit(connection, _event())
    records = list_audit_events(connection)
    assert event_id > 0 and len(records) == 1
    assert records[0].action == "plain_admin_denied" and records[0].trace_id.startswith("trace_")


def test_audit_record_contains_decision_context(connection):
    record_audit(connection, _event(submitted_role="admin", authorization_decision="allow"))
    record = list_audit_events(connection)[0]
    assert record.cookie_name == "lab06_role"
    assert record.submitted_role == "admin" and record.authorization_decision == "allow"


def test_audit_listing_honors_bounded_limit(connection):
    for index in range(3):
        record_audit(connection, _event(action=f"event_{index}"))
    records = list_audit_events(connection, limit=2)
    assert [record.action for record in records] == ["event_2", "event_1"]


def test_audit_text_is_bounded(connection):
    record_audit(connection, _event(reason="x" * 800))
    assert len(list_audit_events(connection)[0].reason) == 500


def test_audit_export_contains_real_records_without_sensitive_fields(connection, tmp_path):
    record_audit(connection, _event())
    destination = export_audit_events(list_audit_events(connection), tmp_path / "audit.json")
    payload = json.loads(destination.read_text(encoding="utf-8"))
    assert payload[0]["action"] == "plain_admin_denied"
    assert "password" not in destination.read_text(encoding="utf-8").lower()
    assert "session_id" not in destination.read_text(encoding="utf-8").lower()


def test_audit_page_is_available_for_inspection(client):
    response = client.get("/audit-logs")
    assert response.status_code == 200

