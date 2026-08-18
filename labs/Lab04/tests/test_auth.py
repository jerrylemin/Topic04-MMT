from database import query_one


def test_login_populates_required_session_fields_and_logout_requires_csrf(client):
    response = client.post("/login", data={"username": "victim", "password": "Victim123!"})
    assert response.status_code in {200, 302, 303}
    with client.session_transaction() as sess:
        assert sess["user_id"] == 10
        assert sess["username"] == "victim"
        assert sess["role"] == "user"
        assert sess["authenticated_at"]
        assert sess["csrf_token"]
        assert sess["csrf_token_issued_at"]
        assert sess["reauthenticated_at"] is None

    denied = client.post(
        "/logout", headers={"Origin": "http://127.0.0.1:5004"}
    )
    assert denied.status_code == 403
    with client.session_transaction() as sess:
        assert sess["user_id"] == 10
        token = sess["csrf_token"]

    response = client.post(
        "/logout",
        data={"csrf_token": token},
        headers={"Origin": "http://127.0.0.1:5004"},
    )
    assert response.status_code == 303
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_bad_login_does_not_authenticate(client):
    response = client.post("/login", data={"username": "victim", "password": "wrong"})
    assert response.status_code == 401
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_demo_password_is_not_plaintext_in_database(app):
    with app.app_context():
        password_hash = query_one("SELECT password_hash FROM users WHERE id = ?", (10,))["password_hash"]
    assert password_hash != "Victim123!"
