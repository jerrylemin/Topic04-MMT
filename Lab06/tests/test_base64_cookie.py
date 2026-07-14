from __future__ import annotations

import base64
import json


def _base64_login(client):
    return client.post(
        "/login",
        data={"username": "student", "password": "Student123!", "mode": "base64"},
        follow_redirects=False,
    )


def _encode(profile):
    raw = json.dumps(profile, ensure_ascii=False, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode()


def test_base64_login_issues_fixed_profile(client):
    response = _base64_login(client)
    cookie = next(
        value
        for value in response.headers.getlist("Set-Cookie")
        if value.startswith("lab06_profile_b64=")
    )
    encoded = cookie.split(";", 1)[0].split("=", 1)[1]
    decoded = json.loads(base64.urlsafe_b64decode(encoded).decode())
    assert decoded == {"username": "student", "role": "user"}


def test_base64_original_profile_is_denied(client):
    _base64_login(client)
    response = client.get("/vulnerable/base64/admin")
    assert response.status_code == 403
    assert response.headers["X-Lab-Decision"] == "deny"


def test_base64_modified_demo_is_allowed(client):
    _base64_login(client)
    client.set_cookie(
        "lab06_profile_b64",
        _encode({"username": "student", "role": "admin"}),
        domain="127.0.0.1",
    )
    response = client.get("/vulnerable/base64/admin")
    assert response.status_code == 200
    assert response.headers["X-Lab-Decision"] == "allow"
    assert "Base64 không phải mã hóa" in response.get_data(as_text=True)


def test_base64_malformed_cookie_is_handled(client):
    client.set_cookie("lab06_profile_b64", "%%%not-base64%%%", domain="127.0.0.1")
    response = client.get("/vulnerable/base64/admin")
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "invalid"


def test_base64_missing_cookie_is_handled(client):
    response = client.get("/vulnerable/base64/admin")
    assert response.status_code == 400
    assert response.headers["X-Lab-Decision"] == "invalid"


def test_base64_trace_reports_no_integrity(client):
    _base64_login(client)
    response = client.get("/vulnerable/base64/admin")
    trace = client.get(f"/api/trace/{response.headers['X-Lab-Trace-ID']}").get_json()
    assert trace["mode"] == "base64"
    assert trace["inspectors"]["base64"]["integrity"] is False
    assert trace["inspectors"]["base64"]["confidentiality"] is False

