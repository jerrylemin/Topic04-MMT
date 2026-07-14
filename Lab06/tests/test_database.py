from __future__ import annotations

import sqlite3

import pytest
from flask import Flask

from database import (
    close_db,
    connect_database,
    execute_parameterized,
    get_db,
    get_user_by_id,
    get_user_by_username,
    init_app,
    initialize_database,
    list_safe_database_stats,
    transaction,
)
from seed import seed_database


@pytest.fixture()
def seeded_db(tmp_path):
    path = seed_database(tmp_path / "database.sqlite3")
    connection = connect_database(path)
    yield connection
    connection.close()


@pytest.mark.parametrize(
    "table",
    ["users", "server_sessions", "audit_logs", "cookie_events", "session_events"],
)
def test_schema_creates_required_tables(tmp_path, table):
    connection = connect_database(tmp_path / "schema.sqlite3")
    initialize_database(connection)
    found = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?", (table,)
    ).fetchone()
    connection.close()
    assert found is not None


def test_connection_enables_foreign_keys(tmp_path):
    connection = connect_database(tmp_path / "foreign-keys.sqlite3")
    assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    connection.close()


def test_user_queries_return_typed_records(seeded_db):
    student = get_user_by_username(seeded_db, "student")
    admin = get_user_by_id(seeded_db, 1)
    assert student is not None and student.id == 10 and student.role == "user"
    assert admin is not None and admin.username == "admin_lab" and admin.role == "admin"


def test_unknown_user_queries_return_none(seeded_db):
    assert get_user_by_id(seeded_db, 9999) is None
    assert get_user_by_username(seeded_db, "absent") is None


def test_transaction_commits_successful_write(seeded_db):
    with transaction(seeded_db, immediate=True):
        seeded_db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("Changed", 10))
    assert seeded_db.execute("SELECT display_name FROM users WHERE id = ?", (10,)).fetchone()[0] == "Changed"


def test_transaction_rolls_back_failed_write(seeded_db):
    with pytest.raises(RuntimeError):
        with transaction(seeded_db, immediate=True):
            seeded_db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("No commit", 10))
            raise RuntimeError("force rollback")
    assert seeded_db.execute("SELECT display_name FROM users WHERE id = ?", (10,)).fetchone()[0] == "Sinh viên Demo"


def test_nested_transaction_uses_savepoint(seeded_db):
    with transaction(seeded_db, immediate=True):
        with transaction(seeded_db):
            seeded_db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("Nested", 10))
    assert get_user_by_id(seeded_db, 10).display_name == "Nested"


def test_nested_transaction_rollback_preserves_outer_transaction(seeded_db):
    with transaction(seeded_db, immediate=True):
        seeded_db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("Outer", 10))
        with pytest.raises(RuntimeError):
            with transaction(seeded_db):
                seeded_db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("Inner", 10))
                raise RuntimeError("rollback savepoint only")
        assert get_user_by_id(seeded_db, 10).display_name == "Outer"
    assert get_user_by_id(seeded_db, 10).display_name == "Outer"


def test_database_stats_expose_counts_not_sensitive_rows(seeded_db):
    stats = list_safe_database_stats(seeded_db)
    assert stats.user_count == 2
    assert stats.session_count == stats.active_session_count == stats.audit_count == 0
    assert not hasattr(stats, "password_hash")


def test_parameterized_helper_rejects_non_tuple_parameters(seeded_db):
    with pytest.raises(TypeError):
        execute_parameterized(seeded_db, "SELECT ?", ["unsafe-shape"])


def test_parameterized_helper_executes_tuple_parameters(seeded_db):
    row = execute_parameterized(seeded_db, "SELECT username FROM users WHERE id = ?", (10,)).fetchone()
    assert row[0] == "student"


def test_sql_injection_string_is_treated_as_data(seeded_db):
    malicious = "student' OR 1=1 --"
    assert get_user_by_username(seeded_db, malicious) is None


def test_flask_database_adapter_reuses_and_closes_request_connection(tmp_path):
    application = Flask("database-adapter-test")
    application.config["DATABASE"] = str(tmp_path / "flask.sqlite3")
    init_app(application)
    with application.app_context():
        first = get_db()
        initialize_database(first)
        assert get_db() is first
        close_db()
        replacement = get_db()
        assert replacement is not first
        assert replacement.execute("SELECT 1").fetchone()[0] == 1


def test_close_db_accepts_teardown_error_and_is_idempotent(tmp_path):
    application = Flask("database-close-test")
    application.config["DATABASE"] = str(tmp_path / "close.sqlite3")
    init_app(application)
    with application.app_context():
        get_db()
        close_db(RuntimeError("teardown"))
        close_db()
