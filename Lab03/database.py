import sqlite3
from pathlib import Path

from flask import current_app, g


def _database_path() -> Path:
    path = Path(current_app.config["DATABASE"])
    return path if path.is_absolute() else Path(current_app.root_path, path)


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(_database_path())
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    schema = Path(current_app.root_path, "schema.sql").read_text(encoding="utf-8")
    get_db().executescript(schema)
    get_db().commit()


def clear_db() -> None:
    db = get_db()
    db.executescript("""
        DROP TABLE IF EXISTS trace_records;
        DROP TABLE IF EXISTS audit_logs;
        DROP TABLE IF EXISTS invoice_items;
        DROP TABLE IF EXISTS invoices;
        DROP TABLE IF EXISTS cart_items;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS users;
    """)
    db.commit()


def query_one(sql: str, parameters: tuple = ()):
    return get_db().execute(sql, parameters).fetchone()


def query_all(sql: str, parameters: tuple = ()):
    return get_db().execute(sql, parameters).fetchall()

