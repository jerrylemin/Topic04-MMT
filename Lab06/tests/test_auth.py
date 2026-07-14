from __future__ import annotations

import pytest

from auth_service import authenticate, require_active_user
from database import connect_database
from seed import seed_database


@pytest.fixture()
def connection(tmp_path):
    conn = connect_database(seed_database(tmp_path / "auth.sqlite3"))
    yield conn
    conn.close()


@pytest.mark.parametrize(
    ("username", "password", "expected_role"),
    [("student", "Student123!", "user"), ("admin_lab", "AdminLab123!", "admin")],
)
def test_authenticate_accepts_demo_credentials(connection, username, password, expected_role):
    result = authenticate(connection, username, password)
    assert result.authenticated is True
    assert result.user is not None and result.user.role == expected_role
    assert result.reason == "password_verified"


@pytest.mark.parametrize(
    ("username", "password"),
    [("student", "wrong"), ("absent", "Student123!"), ("admin_lab", "")],
)
def test_authenticate_rejects_invalid_credentials_without_detail(connection, username, password):
    result = authenticate(connection, username, password)
    assert result.authenticated is False
    assert result.user is None
    assert result.reason == "invalid_credentials"


def test_authenticate_rejects_inactive_user(connection):
    connection.execute("UPDATE users SET active = 0 WHERE id = ?", (10,))
    result = authenticate(connection, "student", "Student123!")
    assert result.authenticated is False
    assert result.user is None


def test_require_active_user_filters_inactive_records(connection):
    assert require_active_user(connection, 10).username == "student"
    connection.execute("UPDATE users SET active = 0 WHERE id = ?", (10,))
    assert require_active_user(connection, 10) is None


def test_authentication_does_not_accept_sql_metacharacters(connection):
    result = authenticate(connection, "student' OR 1=1 --", "Student123!")
    assert result.authenticated is False
