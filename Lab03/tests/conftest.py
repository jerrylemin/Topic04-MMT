import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app


@pytest.fixture()
def app(tmp_path):
    application = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db"), "SECRET_KEY": "test-only"})
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def login(client):
    def do_login(username="user_a", password="UserA123!"):
        response = client.post("/login", data={"username": username, "password": password})
        assert response.status_code == 302
        return response

    return do_login

