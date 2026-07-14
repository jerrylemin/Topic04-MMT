from database import query_one


VICTIM_HEADERS = {"Origin": "http://127.0.0.1:5004"}


def test_reset_requires_valid_csrf_before_changing_state(app, logged_in):
    with app.app_context():
        app.extensions["baseline_email"] = query_one(
            "SELECT email FROM users WHERE id = ?", (10,)
        )["email"]

    denied = logged_in.post("/reset-lab", headers=VICTIM_HEADERS)
    assert denied.status_code == 403
    with logged_in.session_transaction() as sess:
        assert sess["user_id"] == 10
        token = sess["csrf_token"]

    response = logged_in.post(
        "/reset-lab", data={"csrf_token": token}, headers=VICTIM_HEADERS
    )
    assert response.status_code == 303
    with logged_in.session_transaction() as sess:
        assert "user_id" not in sess
