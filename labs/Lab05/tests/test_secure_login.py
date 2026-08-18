from config import AUTH_LOGIC_INPUT, QUOTE_INPUT


def test_same_logic_input_is_data_and_is_rejected(shared_client):
    response = shared_client.post(
        "/secure/login", data={"username": AUTH_LOGIC_INPUT, "password": "wrong"}
    )
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "rejected"
    assert response.headers["X-Lab-Prepared"] == "true"
    assert response.headers["X-Lab-Error-Category"] == "none"


def test_quote_is_bound_as_data_without_database_error(shared_client):
    response = shared_client.post("/secure/login", data={"username": QUOTE_INPUT, "password": "x"})
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "rejected"
    assert response.headers["X-Lab-Error-Category"] == "none"


def test_secure_login_uses_placeholder_and_one_bound_parameter(shared_client):
    response = shared_client.post(
        "/secure/login", data={"username": "student_a", "password": "StudentA123!"}
    )
    trace = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()
    query = trace["query_inspector"]
    assert "?" in query["query_template"]
    assert query["placeholder_count"] == 1
    assert query["parameters_masked"] == ["[BOUND VALUE]"]
    assert query["input_interpreted_as"] == "data"


def test_secure_login_trace_reports_pbkdf2_verification(shared_client):
    response = shared_client.post(
        "/secure/login", data={"username": "student_b", "password": "StudentB123!"}
    )
    auth = shared_client.get(f'/api/trace/{response.headers["X-Lab-Trace-ID"]}').get_json()["decision_inspector"]
    assert auth["password_verification_executed"] is True
    assert auth["password_verification_result"] is True
    assert auth["session_created"] is True


def test_secure_login_rotates_existing_session_payload(shared_client):
    with shared_client.session_transaction() as login_session:
        login_session["untrusted_prelogin_state"] = "must-disappear"
    shared_client.post("/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    with shared_client.session_transaction() as login_session:
        assert "untrusted_prelogin_state" not in login_session
        assert login_session["authenticated_via"] == "secure_pbkdf2"


def test_secure_failure_does_not_disclose_account_existence(shared_client):
    known = shared_client.post("/secure/login", data={"username": "student_a", "password": "wrong"})
    unknown = shared_client.post("/secure/login", data={"username": "nobody", "password": "wrong"})
    assert known.headers["X-Lab-Decision"] == unknown.headers["X-Lab-Decision"] == "rejected"
    assert known.status_code == unknown.status_code == 200

