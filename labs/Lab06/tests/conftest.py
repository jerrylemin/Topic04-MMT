from __future__ import annotations

import sys
from pathlib import Path

import pytest
from cryptography.fernet import Fernet


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def app(tmp_path_factory):
    from app import create_app

    application = create_app(
        {
            "TESTING": True,
            "DATABASE": str(tmp_path_factory.mktemp("lab06") / "lab06-test.sqlite3"),
            "SECRET_KEY": "test-flask-secret-not-for-runtime",
            "SIGNING_KEY": "test-signing-key-not-for-runtime",
            "FERNET_KEY": Fernet.generate_key().decode("ascii"),
            "COOKIE_SECURE": False,
            "SERVER_NAME": "127.0.0.1:5006",
        }
    )
    yield application


@pytest.fixture(autouse=True)
def reset_demo_state(app):
    import sqlite3

    with sqlite3.connect(app.config["DATABASE"]) as connection:
        connection.execute("UPDATE users SET role = 'admin', active = 1 WHERE username = 'admin_lab'")
        connection.execute("UPDATE users SET role = 'user', active = 1 WHERE username = 'student'")
        for table in ("server_sessions", "audit_logs", "cookie_events", "session_events"):
            connection.execute(f"DELETE FROM {table}")
    app.extensions["lab06_traces"].clear()
    yield


@pytest.fixture()
def client(app):
    return app.test_client()
