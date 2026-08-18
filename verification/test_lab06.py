from __future__ import annotations

import base64
import json

import requests

from conftest import local_url, require_service


BASE = local_url(5006)


def login(mode: str, username="student", password="Student123!"):
    session = requests.Session()
    response = session.post(
        BASE + "/login",
        data={"username": username, "password": password, "mode": mode},
        timeout=15,
    )
    assert response.status_code == 200
    return session


def setup_module():
    require_service(5006)
    requests.post(BASE + "/reset-lab", timeout=15)


def test_plain_and_base64_cookie_poisoning_are_demonstrable_locally():
    plain = login("plain")
    assert plain.get(BASE + "/vulnerable/plain/admin", timeout=5).status_code == 403
    plain.cookies.set("lab06_role", "admin", domain="127.0.0.1", path="/")
    assert plain.get(BASE + "/vulnerable/plain/admin", timeout=5).status_code == 200

    encoded = login("base64")
    payload = base64.urlsafe_b64encode(
        json.dumps({"username": "student", "role": "admin"}, separators=(",", ":")).encode()
    ).decode()
    encoded.cookies.set("lab06_profile_b64", payload, domain="127.0.0.1", path="/")
    assert encoded.get(BASE + "/vulnerable/base64/admin", timeout=5).status_code == 200


def test_signed_cookie_tampering_is_rejected():
    session = login("signed")
    assert session.get(BASE + "/secure/signed/profile", timeout=5).status_code == 200
    token = session.cookies.get("lab06_signed_profile")
    assert token
    replacement = ("A" if token[-1] != "A" else "B")
    session.cookies.set("lab06_signed_profile", token[:-1] + replacement, domain="127.0.0.1", path="/")
    assert session.get(BASE + "/secure/signed/profile", timeout=5).status_code in {400, 401, 403}


def test_server_side_session_authorizes_database_role_and_logout_revokes():
    student = login("session")
    assert student.get(BASE + "/secure/session/admin", timeout=5).status_code == 403
    old_cookie = student.cookies.get("lab06_session")
    assert old_cookie
    assert student.post(BASE + "/secure/session/logout", timeout=10).status_code == 200
    assert student.get(BASE + "/secure/session/profile", timeout=5).status_code in {401, 403}
    admin = login("session", "admin_lab", "AdminLab123!")
    assert admin.get(BASE + "/secure/session/admin", timeout=5).status_code == 200
    assert requests.get("http://localhost:5006/health", timeout=5).status_code == 200
