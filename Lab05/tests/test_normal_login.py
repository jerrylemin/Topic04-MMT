import pytest


@pytest.mark.parametrize("route,via", [
    ("/vulnerable/login", "vulnerable_local_demo"),
    ("/secure/login", "secure_pbkdf2"),
])
def test_demo_admin_can_log_in_with_documented_credentials(shared_client, route, via):
    response = shared_client.post(route, data={"username": "admin_lab", "password": "AdminLab123!"})
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "authenticated"
    with shared_client.session_transaction() as login_session:
        assert login_session["user_id"] == 1
        assert login_session["username"] == "admin_lab"
        assert login_session["role"] == "admin"
        assert login_session["authenticated_via"] == via


@pytest.mark.parametrize("route", ["/vulnerable/login", "/secure/login"])
def test_normal_wrong_password_does_not_create_session(shared_client, route):
    response = shared_client.post(route, data={"username": "student_a", "password": "wrong"})
    assert response.headers["X-Lab-Decision"] == "rejected"
    with shared_client.session_transaction() as login_session:
        assert "user_id" not in login_session


def test_logout_clears_authenticated_session(shared_client):
    shared_client.post("/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"})
    assert shared_client.post("/logout").get_json() == {"logged_out": True}
    with shared_client.session_transaction() as login_session:
        assert not login_session

