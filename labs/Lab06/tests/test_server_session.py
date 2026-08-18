from __future__ import annotations

import hashlib
import sqlite3


def _login(client, username="student", password="Student123!"):
    return client.post(
        "/login",
        data={"username": username, "password": password, "mode": "session"},
        follow_redirects=False,
    )


def _cookie_value(response, name="lab06_session"):
    header = next(
        value
        for value in response.headers.getlist("Set-Cookie")
        if value.startswith(f"{name}=")
    )
    return header.split(";", 1)[0].split("=", 1)[1]


def test_session_login_issues_opaque_httponly_cookie(client):
    response = _login(client)
    token = _cookie_value(response)
    assert len(token) >= 40
    assert "user" not in token
    assert "admin" not in token
    cookie = next(x for x in response.headers.getlist("Set-Cookie") if x.startswith("lab06_session="))
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie


def test_session_database_stores_hash_not_raw(app, client):
    token = _cookie_value(_login(client))
    with sqlite3.connect(app.config["DATABASE"]) as connection:
        stored = connection.execute(
            "SELECT session_token_hash FROM server_sessions ORDER BY id DESC LIMIT 1"
        ).fetchone()[0]
        dump = " ".join(
            str(value)
            for row in connection.execute("SELECT * FROM server_sessions")
            for value in row
        )
    assert stored == hashlib.sha256(token.encode()).hexdigest()
    assert token not in dump


def test_student_session_is_denied_admin(client):
    _login(client)
    response = client.get("/secure/session/admin")
    assert response.status_code == 403
    assert response.headers["X-Lab-Role-Source"] == "database"


def test_admin_session_is_allowed_admin(client):
    _login(client, "admin_lab", "AdminLab123!")
    response = client.get("/secure/session/admin")
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "allow"


def test_database_role_change_applies_next_request(app, client):
    _login(client, "admin_lab", "AdminLab123!")
    assert client.get("/secure/session/admin").status_code == 200
    with sqlite3.connect(app.config["DATABASE"]) as connection:
        connection.execute("UPDATE users SET role = 'user' WHERE username = 'admin_lab'")
    assert client.get("/secure/session/admin").status_code == 403


def test_session_rotation_replaces_and_revokes_old_token(client):
    old_token = _cookie_value(_login(client))
    new_token = _cookie_value(_login(client))
    assert new_token != old_token
    client.set_cookie("lab06_session", old_token, domain="127.0.0.1")
    response = client.get("/secure/session/profile")
    assert response.status_code == 401
    assert response.headers["X-Lab-Session-Status"] == "inactive_session"


def test_logout_revokes_server_record_and_expires_cookie(client):
    old_token = _cookie_value(_login(client))
    response = client.post("/secure/session/logout")
    assert response.status_code == 200
    expired = next(x for x in response.headers.getlist("Set-Cookie") if x.startswith("lab06_session="))
    assert "Max-Age=0" in expired
    client.set_cookie("lab06_session", old_token, domain="127.0.0.1")
    assert client.get("/secure/session/profile").status_code == 401


def test_missing_session_is_rejected(client):
    response = client.get("/secure/session/profile")
    assert response.status_code == 401
    assert response.headers["X-Lab-Session-Status"] == "missing_session_cookie"

