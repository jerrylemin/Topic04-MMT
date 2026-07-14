from database import query_one


VICTIM_HEADERS = {"Origin": "http://127.0.0.1:5004"}


def _token(client):
    with client.session_transaction() as sess:
        return sess["csrf_token"]


def _email(app):
    with app.app_context():
        return query_one("SELECT email FROM users WHERE id = ?", (10,))["email"]


def test_secure_email_rejects_missing_and_invalid_tokens_before_state_change(app, logged_in):
    assert logged_in.post("/secure/change-email", data={"email": "missing@lab.local"}, headers=VICTIM_HEADERS).status_code == 403
    assert _email(app) == "victim_old@lab.local"

    response = logged_in.post(
        "/secure/change-email",
        data={"email": "invalid@lab.local", "csrf_token": "x" * 43},
        headers=VICTIM_HEADERS,
    )
    assert response.status_code == 403
    assert _email(app) == "victim_old@lab.local"


def test_secure_email_accepts_valid_token_then_rotates_it(app, logged_in):
    old_token = _token(logged_in)
    response = logged_in.post(
        "/secure/change-email",
        data={"email": "victim_new@lab.local", "csrf_token": old_token},
        headers=VICTIM_HEADERS,
    )
    assert response.status_code == 200
    assert _email(app) == "victim_new@lab.local"
    assert _token(logged_in) != old_token


def test_secure_email_rejects_attacker_origin_even_with_valid_token(app, logged_in):
    response = logged_in.post(
        "/secure/change-email",
        data={"email": "blocked@lab.local", "csrf_token": _token(logged_in)},
        headers={"Origin": "http://127.0.0.1:9004"},
    )
    assert response.status_code == 403
    assert _email(app) == "victim_old@lab.local"


def test_secure_email_rejects_duplicate_demo_address_without_state_change(app, logged_in):
    response = logged_in.post(
        "/secure/change-email",
        data={"email": "receiver@lab.local", "csrf_token": _token(logged_in)},
        headers=VICTIM_HEADERS,
    )
    assert response.status_code == 400
    assert _email(app) == "victim_old@lab.local"
