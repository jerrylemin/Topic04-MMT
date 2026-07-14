import sqlite3

import pytest

from database import execute_read_only, get_db, query_all, query_one


@pytest.mark.parametrize("table", [
    "users", "products", "audit_logs", "login_attempts", "query_events", "trace_records",
])
def test_required_tables_exist(shared_app, table):
    with shared_app.app_context():
        columns = query_all(f"PRAGMA table_info({table})")
    assert columns, f"missing table {table}"


def test_database_rows_are_mapping_accessible(shared_app):
    with shared_app.app_context():
        row = query_one("SELECT id, username FROM users ORDER BY id LIMIT 1")
    assert row["id"] == 1
    assert row["username"] == "admin_lab"


def test_read_only_executor_rejects_write_statement(shared_app):
    with shared_app.app_context(), pytest.raises(ValueError, match="read-only"):
        execute_read_only("UPDATE products SET stock = 0")


def test_sqlite_execute_rejects_stacked_statements(shared_app):
    with shared_app.app_context(), pytest.raises(sqlite3.ProgrammingError):
        execute_read_only("SELECT id FROM products; SELECT id FROM users")


def test_foreign_keys_are_enabled(shared_app):
    with shared_app.app_context():
        assert get_db().execute("PRAGMA foreign_keys").fetchone()[0] == 1

