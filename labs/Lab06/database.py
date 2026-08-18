from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from flask import Flask, current_app, g


SCHEMA_PATH = Path(__file__).with_name("schema.sql")


@dataclass(frozen=True, slots=True)
class UserRecord:
    id: int
    username: str
    display_name: str
    email: str
    password_hash: str
    role: str
    active: bool
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class DatabaseStats:
    user_count: int
    session_count: int
    active_session_count: int
    audit_count: int


def connect_database(path: str | Path) -> sqlite3.Connection:
    database_path = Path(path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(database_path), timeout=5.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = connect_database(current_app.config["DATABASE"])
    return g.db


def close_db(error: BaseException | None = None) -> None:
    del error
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)


def initialize_database(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


init_database = initialize_database


@contextmanager
def transaction(
    conn: sqlite3.Connection, *, immediate: bool = False
) -> Iterator[sqlite3.Connection]:
    if conn.in_transaction:
        savepoint = f"sp_{id(conn):x}"
        conn.execute(f"SAVEPOINT {savepoint}")
        try:
            yield conn
        except BaseException:
            conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
            raise
        else:
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        return
    conn.execute("BEGIN IMMEDIATE" if immediate else "BEGIN")
    try:
        yield conn
    except BaseException:
        conn.rollback()
        raise
    else:
        conn.commit()


def _user_from_row(row: sqlite3.Row | None) -> UserRecord | None:
    if row is None:
        return None
    return UserRecord(
        id=int(row["id"]), username=str(row["username"]),
        display_name=str(row["display_name"]), email=str(row["email"]),
        password_hash=str(row["password_hash"]), role=str(row["role"]),
        active=bool(row["active"]), created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


# LAB06-CODE:database_role_lookup:START
def get_user_by_id(conn: sqlite3.Connection, user_id: int) -> UserRecord | None:
    row = conn.execute(
        "SELECT id, username, display_name, email, password_hash, role, active, "
        "created_at, updated_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    return _user_from_row(row)
# LAB06-CODE:database_role_lookup:END


def get_user_by_username(conn: sqlite3.Connection, username: str) -> UserRecord | None:
    row = conn.execute(
        "SELECT id, username, display_name, email, password_hash, role, active, "
        "created_at, updated_at FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    return _user_from_row(row)


def list_safe_database_stats(conn: sqlite3.Connection) -> DatabaseStats:
    row = conn.execute(
        "SELECT (SELECT COUNT(*) FROM users) AS users, "
        "(SELECT COUNT(*) FROM server_sessions) AS sessions, "
        "(SELECT COUNT(*) FROM server_sessions WHERE active = 1) AS active_sessions, "
        "(SELECT COUNT(*) FROM audit_logs) AS audits"
    ).fetchone()
    return DatabaseStats(int(row["users"]), int(row["sessions"]), int(row["active_sessions"]), int(row["audits"]))


def execute_parameterized(
    conn: sqlite3.Connection, sql: str, parameters: tuple[Any, ...] = ()
) -> sqlite3.Cursor:
    if not isinstance(parameters, tuple):
        raise TypeError("SQL parameters must be supplied as a tuple")
    return conn.execute(sql, parameters)
