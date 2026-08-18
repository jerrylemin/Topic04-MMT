from config import AUTH_LOGIC_INPUT, QUOTE_INPUT


def test_quote_scenario_records_handled_sql_error(shared_client):
    response = shared_client.post("/vulnerable/login", data={"username": QUOTE_INPUT, "password": "x"})
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "query_error"
    assert response.headers["X-Lab-Error-Category"] == "sql_syntax_error"
    assert b"Traceback" not in response.data


def test_fixed_authentication_logic_scenario_creates_labeled_demo_session(shared_client):
    response = shared_client.post(
        "/vulnerable/login", data={"username": AUTH_LOGIC_INPUT, "password": "not-the-admin-password"}
    )
    assert response.headers["X-Lab-Decision"] == "local_demo_bypass"
    with shared_client.session_transaction() as login_session:
        assert login_session["user_id"] == 1
        assert login_session["authenticated_via"] == "vulnerable_local_demo"


def test_unapproved_sql_shaped_username_is_blocked_before_query(shared_client):
    response = shared_client.post(
        "/vulnerable/login", data={"username": "student_a' OR 'a'='a", "password": "x"}
    )
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "validation_failed"


def test_vulnerable_login_trace_marks_string_concatenation(shared_client):
    response = shared_client.post(
        "/vulnerable/login", data={"username": "student_b", "password": "StudentB123!"}
    )
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    assert trace["query_inspector"]["construction_method"] == "string_concatenation"
    assert trace["query_inspector"]["prepared"] is False
    assert trace["final_verdict"]["database_modified"] is False


def test_vulnerable_login_query_evidence_masks_legacy_digest(shared_app, shared_client):
    response = shared_client.post(
        "/vulnerable/login", data={"username": "admin_lab", "password": "AdminLab123!"}
    )
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    final_query = trace["query_inspector"]["final_query_masked"]
    assert "AdminLab123!" not in final_query
    assert "[REDACTED]" in final_query

