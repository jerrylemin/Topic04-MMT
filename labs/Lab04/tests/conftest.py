from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from database import query_one
from seed import reset_database
from victim_app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-secret",
        "DATABASE": str(tmp_path / "lab04.sqlite3"),
    })
    with app.app_context():
        reset_database()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def login(client):
    def _login(username="victim", password="Victim123!"):
        return client.post("/login", data={"username": username, "password": password})
    return _login


@pytest.fixture
def logged_in(client, login):
    login()
    return client


@pytest.fixture
def victim(app):
    with app.app_context():
        return dict(query_one("SELECT * FROM users WHERE username = ?", ("victim",)))
