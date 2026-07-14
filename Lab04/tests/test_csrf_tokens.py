from csrf_service import (
    ensure_csrf_token,
    generate_csrf_token,
    mask_csrf_token,
    validate_csrf_token,
)


def test_tokens_are_random_and_checked_by_status():
    first = generate_csrf_token()
    second = generate_csrf_token()
    assert first != second
    assert len(first) >= 32
    assert validate_csrf_token(first, None) == {
        "present": False,
        "valid": False,
        "status": "missing",
        "reason": "token_missing",
    }
    assert validate_csrf_token(first, "short")["status"] == "invalid"
    assert validate_csrf_token(first, second)["valid"] is False
    assert validate_csrf_token(first, first)["valid"] is True
    assert mask_csrf_token(first) != first


def test_ensure_csrf_token_reuses_the_current_session_token(app):
    with app.test_request_context("/"):
        first = ensure_csrf_token()
        assert ensure_csrf_token() == first


def test_two_logins_receive_different_session_tokens(app):
    first = app.test_client()
    second = app.test_client()
    first.post("/login", data={"username": "victim", "password": "Victim123!"})
    second.post("/login", data={"username": "victim", "password": "Victim123!"})
    with first.session_transaction() as one, second.session_transaction() as two:
        assert one["csrf_token"] != two["csrf_token"]
