from __future__ import annotations

import re

import requests

from conftest import local_url, require_service


BASE = local_url(5004)
ATTACKER = local_url(9004)


def login():
    session = requests.Session()
    response = session.post(BASE + "/login", data={"username": "victim", "password": "Victim123!"}, timeout=10)
    assert response.status_code == 200 and response.url.endswith("/dashboard")
    return session


def csrf_token(html: str) -> str:
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    assert match, "CSRF token is absent from secure form"
    return match.group(1)


def setup_module():
    require_service(5004)
    require_service(9004)


def test_vulnerable_cross_origin_request_changes_state():
    session = login()
    session.post(BASE + "/reset-lab", timeout=10)
    response = session.post(
        BASE + "/vulnerable/change-email",
        data={"email": "csrf_vulnerable@lab.local"},
        headers={"Origin": ATTACKER}, timeout=5,
    )
    assert response.status_code == 200 and "csrf_vulnerable@lab.local" in response.text


def test_secure_missing_or_wrong_origin_is_rejected_then_valid_token_succeeds():
    session = login()
    session.post(BASE + "/reset-lab", timeout=10)
    missing = session.post(
        BASE + "/secure/change-email",
        data={"email": "must_not_change@lab.local"},
        headers={"Origin": ATTACKER}, timeout=5,
    )
    assert missing.status_code == 403
    form = session.get(BASE + "/secure/change-email", timeout=5)
    token = csrf_token(form.text)
    allowed = session.post(
        BASE + "/secure/change-email",
        data={"email": "csrf_secure@lab.local", "csrf_token": token},
        headers={"Origin": BASE}, timeout=5,
    )
    assert allowed.status_code == 200 and "csrf_secure@lab.local" in allowed.text


def test_both_loopback_aliases_render():
    assert requests.get("http://localhost:5004/health", timeout=5).status_code == 200
    assert requests.get("http://localhost:9004/health", timeout=5).status_code == 200

