from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta

import pytest

from database import connect_database
from seed import seed_database
from server_session_service import (
    generate_session_token,
    hash_session_token,
    resolve_session,
    revoke_all_demo_sessions,
    rotate_session,
)


@pytest.fixture()
def connection(tmp_path):
    conn = connect_database(seed_database(tmp_path / "sessions.sqlite3"))
    yield conn
    conn.close()


def _issue(connection, user_id=10, previous=None, now=None):
    return rotate_session(
        connection,
        user_id=user_id,
        previous_raw_token=previous,
        now=now or datetime.now(UTC),
        ttl=timedelta(minutes=30),
        trace_id="trace_0123456789abcdef01234567",
        reason="login_rotation",
    )


def test_generated_session_tokens_are_random_and_url_safe():
    first, second = generate_session_token(), generate_session_token()
    assert first != second
    assert len(first) >= 40 and len(second) >= 40
    assert all(character.isalnum() or character in "-_" for character in first)


def test_hash_session_token_is_sha256():
    token = "opaque-session-token"
    assert hash_session_token(token) == hashlib.sha256(token.encode()).hexdigest()
    assert len(hash_session_token(token)) == 64


def test_rotation_stores_hash_and_not_raw_token(connection):
    issue = _issue(connection)
    row = connection.execute("SELECT session_token_hash FROM server_sessions").fetchone()
    assert row[0] == hash_session_token(issue.raw_token)
    assert issue.raw_token not in " ".join(str(value) for value in row)


def test_rotation_invalidates_previous_token(connection):
    old = _issue(connection)
    new = _issue(connection, previous=old.raw_token)
    assert new.raw_token != old.raw_token
    assert resolve_session(connection, old.raw_token, datetime.now(UTC)).reason == "inactive_session"
    assert resolve_session(connection, new.raw_token, datetime.now(UTC)).valid


def test_rotation_records_old_and_new_fingerprints(connection):
    old = _issue(connection)
    _issue(connection, previous=old.raw_token)
    row = connection.execute(
        "SELECT event_type, old_session_fingerprint, new_session_fingerprint "
        "FROM session_events ORDER BY id DESC LIMIT 1"
    ).fetchone()
    assert row[0] == "server_session_rotated"
    assert row[1] and row[2] and row[1] != row[2]


def test_resolve_unknown_token_does_not_create_record(connection):
    result = resolve_session(connection, "unknown-token", datetime.now(UTC))
    assert not result.valid and result.reason == "unknown_session"
    assert connection.execute("SELECT COUNT(*) FROM server_sessions").fetchone()[0] == 0


def test_resolve_expired_session_marks_record_inactive(connection):
    past = datetime.now(UTC) - timedelta(hours=1)
    issue = rotate_session(
        connection, user_id=10, previous_raw_token=None, now=past,
        ttl=timedelta(seconds=1), trace_id="trace_0123456789abcdef01234567",
    )
    result = resolve_session(connection, issue.raw_token, datetime.now(UTC))
    assert not result.valid and result.reason == "expired_session" and not result.active
    assert connection.execute("SELECT active FROM server_sessions").fetchone()[0] == 0


def test_resolve_reloads_current_database_role(connection):
    issue = _issue(connection, user_id=1)
    assert resolve_session(connection, issue.raw_token, datetime.now(UTC)).database_role == "admin"
    connection.execute("UPDATE users SET role = ? WHERE id = ?", ("user", 1))
    assert resolve_session(connection, issue.raw_token, datetime.now(UTC)).database_role == "user"


def test_reset_revokes_every_active_demo_session(connection):
    _issue(connection, user_id=10)
    _issue(connection, user_id=1)
    count = revoke_all_demo_sessions(
        connection,
        now=datetime.now(UTC),
        trace_id="trace_0123456789abcdef01234567",
    )
    assert count == 2
    assert connection.execute("SELECT COUNT(*) FROM server_sessions WHERE active = 1").fetchone()[0] == 0

