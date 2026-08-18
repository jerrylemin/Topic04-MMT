import sqlite3
from contextlib import contextmanager
from pathlib import Path

from flask import current_app, g


def database_path() -> Path:
    path = Path(current_app.config["DATABASE"])
    return path if path.is_absolute() else Path(current_app.root_path, path)


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        path = database_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
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


def query_one(sql: str, parameters: tuple = ()):
    return get_db().execute(sql, parameters).fetchone()


def query_all(sql: str, parameters: tuple = ()):
    return get_db().execute(sql, parameters).fetchall()


def execute(sql: str, parameters: tuple = ()) -> sqlite3.Cursor:
    cursor = get_db().execute(sql, parameters)
    get_db().commit()
    return cursor


@contextmanager
def transaction():
    db = get_db()
    try:
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise

