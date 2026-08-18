from database import query_one
from werkzeug.security import check_password_hash


def _token(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


def test_secure_password_requires_csrf_origin_and_current_password(app, logged_in):
    response = logged_in.post(
        "/secure/change-password",
        data={"csrf_token": _token(logged_in), "current_password": "wrong", "new_password": "NewPassword123!"},
        headers={"Origin": "http://127.0.0.1:5004"},
    )
    assert response.status_code == 403

    response = logged_in.post(
        "/secure/change-password",
        data={"csrf_token": _token(logged_in), "current_password": "Victim123!", "new_password": "NewPassword123!"},
        headers={"Origin": "http://127.0.0.1:5004"},
    )
    assert response.status_code == 200
    with app.app_context():
        password_hash = query_one("SELECT password_hash FROM users WHERE id = ?", (10,))["password_hash"]
    assert check_password_hash(password_hash, "NewPassword123!")

