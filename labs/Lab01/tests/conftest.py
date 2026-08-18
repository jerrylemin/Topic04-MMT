import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
import pytest
from app import create_app
from database import reset_db
@pytest.fixture()
def app(tmp_path):
    app=create_app({"TESTING":True,"DATABASE":str(tmp_path/"test.db")})
    with app.app_context(): reset_db()
    yield app
@pytest.fixture()
def client(app): return app.test_client()
