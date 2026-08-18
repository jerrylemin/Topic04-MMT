from __future__ import annotations


def _plain_login(client):
    return client.post(
        "/login",
        data={"username": "student", "password": "Student123!", "mode": "plain"},
        follow_redirects=False,
    )


def test_plain_login_issues_fixed_username_cookie(client):
    response = _plain_login(client)
    cookies = response.headers.getlist("Set-Cookie")
    assert any(value.startswith("lab06_username=student") for value in cookies)


def test_plain_login_issues_user_role_cookie(client):
    response = _plain_login(client)
    cookies = response.headers.getlist("Set-Cookie")
    role = next(value for value in cookies if value.startswith("lab06_role="))
    assert role.startswith("lab06_role=user")
    assert "Path=/" in role
    assert "SameSite=Lax" in role
    assert "HttpOnly" not in role


def test_plain_user_cookie_is_denied_admin(client):
    _plain_login(client)
    response = client.get("/vulnerable/plain/admin")
    assert response.status_code == 403
    assert response.headers["X-Lab-Decision"] == "deny"


def test_plain_admin_cookie_is_allowed_in_local_demo(client):
    _plain_login(client)
    client.set_cookie("lab06_role", "admin", domain="127.0.0.1")
    response = client.get("/vulnerable/plain/admin")
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "allow"
    assert "tin cookie phía client" in response.get_data(as_text=True)


def test_plain_flow_emits_trace_identifier(client):
    _plain_login(client)
    response = client.get("/vulnerable/plain/admin")
    trace_id = response.headers.get("X-Lab-Trace-ID")
    assert trace_id
    trace = client.get(f"/api/trace/{trace_id}")
    assert trace.status_code == 200
    assert trace.get_json()["mode"] == "plain"

