import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from config import AUTH_LOGIC_INPUT, QUOTE_INPUT, SEARCH_EXPANDED_INPUT
from database import query_all, query_one
from seed import reset_database


@pytest.fixture()
def app(tmp_path):
    application = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-only-secret",
        "DATABASE": str(tmp_path / "lab05.sqlite3"),
    })
    with application.app_context():
        reset_database()
    return application


@pytest.fixture()
def client(app):
    return app.test_client()


def test_seed_uses_pbkdf2_and_never_plaintext(app):
    with app.app_context():
        users = [dict(row) for row in query_all("SELECT * FROM users ORDER BY id")]
        products = query_all("SELECT * FROM products")
    assert len(users) == 3
    assert len(products) >= 8
    assert all(user["password_hash"].startswith("pbkdf2:sha256:600000$") for user in users)
    serialized = json.dumps(users)
    assert "AdminLab123!" not in serialized
    assert "StudentA123!" not in serialized


def test_vulnerable_and_secure_login_vertical_slice(app, client):
    normal = client.post("/vulnerable/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    assert normal.status_code == 200
    assert normal.headers["X-Lab-Decision"] == "authenticated"

    client.post("/logout")
    quote = client.post("/vulnerable/login", data={"username": QUOTE_INPUT, "password": "x"})
    assert quote.status_code == 200
    assert quote.headers["X-Lab-Error-Category"] == "sql_syntax_error"

    bypass = client.post("/vulnerable/login", data={"username": AUTH_LOGIC_INPUT, "password": "wrong"})
    assert bypass.headers["X-Lab-Decision"] == "local_demo_bypass"
    with client.session_transaction() as session:
        assert session["authenticated_via"] == "vulnerable_local_demo"

    client.post("/logout")
    rejected = client.post("/secure/login", data={"username": AUTH_LOGIC_INPUT, "password": "wrong"})
    assert rejected.headers["X-Lab-Decision"] == "rejected"
    with client.session_transaction() as session:
        assert "user_id" not in session

    secure = client.post("/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    assert secure.headers["X-Lab-Decision"] == "authenticated"
    with client.session_transaction() as session:
        assert session["authenticated_via"] == "secure_pbkdf2"

    with app.app_context():
        assert query_one("SELECT COUNT(*) AS count FROM audit_logs")["count"] >= 5
        payloads = [row["payload"] for row in query_all("SELECT payload FROM trace_records")]
        password_hash = query_one("SELECT password_hash FROM users WHERE username = ?", ("admin_lab",))["password_hash"]
    assert payloads
    assert all("AdminLab123!" not in payload and "wrong" not in payload for payload in payloads)
    assert password_hash not in secure.get_data(as_text=True)


def test_search_fixed_scenarios_and_parameterized_secure_route(client):
    normal = client.get("/vulnerable/search", query_string={"keyword": "USB"})
    assert normal.status_code == 200
    normal_count = int(normal.headers["X-Lab-Result-Count"])
    assert normal_count >= 1

    quote = client.get("/vulnerable/search", query_string={"keyword": QUOTE_INPUT})
    assert quote.headers["X-Lab-Error-Category"] == "sql_syntax_error"

    expanded = client.get("/vulnerable/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    assert int(expanded.headers["X-Lab-Result-Count"]) > normal_count

    secure = client.get("/secure/search", query_string={"keyword": SEARCH_EXPANDED_INPUT})
    assert secure.status_code == 200
    assert secure.headers["X-Lab-Prepared"] == "true"
    assert int(secure.headers["X-Lab-Result-Count"]) == 0


def test_public_routes_headers_trace_and_runtime_restrictions(app, client):
    for path in ("/", "/dashboard", "/comparison", "/security-controls", "/audit-logs", "/health"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert "unsafe-eval" not in response.headers["Content-Security-Policy"]

    detail = client.get("/secure/user?id=1")
    assert detail.status_code == 200
    assert detail.headers["X-Lab-Prepared"] == "true"
    invalid = client.get("/secure/user?id=not-a-number")
    assert invalid.status_code == 400

    with app.app_context():
        trace_id = query_one("SELECT trace_id FROM trace_records ORDER BY created_at DESC LIMIT 1")["trace_id"]
    trace = client.get(f"/api/trace/{trace_id}")
    assert trace.status_code == 200
    body = trace.get_json()
    assert body["trace_id"] == trace_id
    assert body["steps"]
    assert {"technique", "input_data", "output_data", "code_reference"} <= body["steps"][0].keys()

    assert app.config["SERVER_HOST"] == "127.0.0.1"
    assert app.config["SERVER_PORT"] == 5005
    assert app.debug is False


def test_unapproved_sql_shaped_inputs_are_not_executed(client):
    response = client.post(
        "/vulnerable/login",
        data={"username": "admin_lab' OR 'x'='x", "password": "x"},
    )
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "validation_failed"


def test_trace_contract_matches_each_explicit_flow(app, client):
    responses = [
        client.post("/vulnerable/login", data={"username": QUOTE_INPUT, "password": "x"}),
        client.post("/secure/login", data={"username": AUTH_LOGIC_INPUT, "password": "x"}),
        client.get("/vulnerable/search", query_string={"keyword": SEARCH_EXPANDED_INPUT}),
        client.get("/secure/search", query_string={"keyword": SEARCH_EXPANDED_INPUT}),
    ]
    expected_lengths = [12, 10, 9, 7]
    for response, expected in zip(responses, expected_lengths):
        trace = client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
        assert len(trace["steps"]) == expected
        assert trace["request_inspector"]["timestamp"]
        assert trace["steps"][-1]["layer"] == "Final Result"

    vulnerable_login_trace = client.get(
        f'/api/trace/{responses[0].headers["X-Lab-Trace-ID"]}'
    ).get_json()
    auth = vulnerable_login_trace["decision_inspector"]
    assert auth["username_submitted"] == QUOTE_INPUT
    assert auth["password_length"] == 1
    assert auth["password_fingerprint"] == "[NOT STORED]"
    assert {"user_matched", "password_verification_executed", "password_verification_result",
            "session_created", "final_decision"} <= auth.keys()
    error = vulnerable_login_trace["error_inspector"]
    assert {"query_template", "input_insertion", "root_cause", "data_modified"} <= error.keys()
    assert error["data_modified"] is False
