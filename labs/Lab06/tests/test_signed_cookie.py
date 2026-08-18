from __future__ import annotations


def _login(client, username="student", password="Student123!"):
    return client.post(
        "/login",
        data={"username": username, "password": password, "mode": "signed"},
        follow_redirects=False,
    )


def _cookie_value(response, name="lab06_signed_profile"):
    header = next(
        value
        for value in response.headers.getlist("Set-Cookie")
        if value.startswith(f"{name}=")
    )
    return header.split(";", 1)[0].split("=", 1)[1]


def _mutate(value):
    index = max(1, len(value) // 3)
    replacement = "A" if value[index] != "A" else "B"
    return value[:index] + replacement + value[index + 1 :]


def test_signed_login_sets_httponly_cookie(client):
    response = _login(client)
    cookie = next(
        value
        for value in response.headers.getlist("Set-Cookie")
        if value.startswith("lab06_signed_profile=")
    )
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie
    assert "Path=/" in cookie


def test_signed_valid_profile_is_accepted(client):
    _login(client)
    response = client.get("/secure/signed/profile")
    assert response.status_code == 200
    assert response.headers["X-Lab-Signature-Status"] == "valid"


def test_signed_student_is_denied_admin_from_database(client):
    _login(client)
    response = client.get("/secure/signed/admin")
    assert response.status_code == 403
    assert response.headers["X-Lab-Decision"] == "deny"
    assert response.headers["X-Lab-Role-Source"] == "database"


def test_signed_admin_is_allowed_from_database(client):
    _login(client, "admin_lab", "AdminLab123!")
    response = client.get("/secure/signed/admin")
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "allow"
    assert response.headers["X-Lab-Role-Source"] == "database"


def test_signed_payload_mutation_is_rejected(client):
    login = _login(client)
    client.set_cookie(
        "lab06_signed_profile",
        _mutate(_cookie_value(login)),
        domain="127.0.0.1",
    )
    response = client.get("/secure/signed/profile")
    assert response.status_code == 400
    assert response.headers["X-Lab-Signature-Status"] == "invalid"


def test_signed_signature_mutation_is_rejected(client):
    login = _login(client)
    token = _cookie_value(login)
    client.set_cookie(
        "lab06_signed_profile",
        token[:-1] + ("A" if token[-1] != "A" else "B"),
        domain="127.0.0.1",
    )
    response = client.get("/secure/signed/profile")
    assert response.status_code == 400
    assert response.headers["X-Lab-Signature-Status"] == "invalid"


def test_signed_missing_cookie_is_rejected(client):
    response = client.get("/secure/signed/profile")
    assert response.status_code == 401
    assert response.headers["X-Lab-Signature-Status"] == "missing"

