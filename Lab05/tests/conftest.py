import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app
from database import get_db


@pytest.fixture(scope="session")
def shared_app(tmp_path_factory):
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "shared-test-only-secret",
        "DATABASE": str(tmp_path_factory.mktemp("lab05") / "suite.sqlite3"),
        "SERVER_NAME": "127.0.0.1:5005",
    })
    return app


@pytest.fixture()
def shared_client(shared_app):
    return shared_app.test_client()


@pytest.fixture()
def clear_events(shared_app):
    with shared_app.app_context():
        db = get_db()
        db.executescript("""
            DELETE FROM audit_logs;
            DELETE FROM login_attempts;
            DELETE FROM query_events;
            DELETE FROM trace_records;
        """)
        db.commit()
    yield

