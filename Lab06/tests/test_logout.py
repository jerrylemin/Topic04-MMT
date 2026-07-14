from __future__ import annotations

import sqlite3


def _login(client):
    return client.post(
        "/login",
        data={"username": "student", "password": "Student123!", "mode": "session"},
        follow_redirects=False,
    )


def _token(response):
    header = next(value for value in response.headers.getlist("Set-Cookie") if value.startswith("lab06_session="))
    return header.split(";", 1)[0].split("=", 1)[1]


def test_common_logout_revokes_server_side_record(app, client):
    token = _token(_login(client))
    response = client.post("/logout")
    assert response.status_code == 200
    with sqlite3.connect(app.config["DATABASE"]) as connection:
        active = connection.execute(
            "SELECT active FROM server_sessions WHERE session_token_hash = ?",
            (__import__("hashlib").sha256(token.encode()).hexdigest(),),
        ).fetchone()[0]
    assert active == 0


def test_logout_without_session_is_idempotent(client):
    response = client.post("/logout")
    assert response.status_code == 200
    assert response.headers["X-Lab-Session-Status"] == "no_active_session"


def test_logout_is_not_available_via_get(client):
    assert client.get("/logout").status_code == 405


def test_old_token_is_rejected_after_logout(client):
    token = _token(_login(client))
    client.post("/secure/session/logout")
    client.set_cookie("lab06_session", token, domain="127.0.0.1")
    response = client.get("/secure/session/profile")
    assert response.status_code == 401
    assert response.headers["X-Lab-Session-Status"] == "inactive_session"

