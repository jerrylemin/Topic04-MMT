from __future__ import annotations

import requests

from conftest import local_url, require_service


BASE = local_url(5003)


def login(username="user_a", password="UserA123!"):
    session = requests.Session()
    response = session.post(BASE + "/login", data={"username": username, "password": password}, timeout=10)
    assert response.status_code == 200 and response.url.endswith("/products")
    return session


def setup_module():
    require_service(5003)
    requests.post(BASE + "/reset-lab", timeout=10)


def test_all_demo_accounts_and_cookie_session_login():
    for credentials in (("user_a", "UserA123!"), ("user_b", "UserB123!"), ("admin", "Admin123!")):
        session = login(*credentials)
        assert session.cookies and session.get(BASE + "/cart", timeout=5).status_code == 200


def test_price_tampering_pair_and_idor_pair():
    session = login()
    session.post(BASE + "/cart/add", data={"product_id": 5, "quantity": 1}, timeout=5)
    vulnerable = session.post(
        BASE + "/vulnerable/checkout",
        data={"product_id": 5, "quantity": 1, "price": 1}, timeout=5,
    )
    secure = session.post(
        BASE + "/secure/checkout",
        data={"product_id": 5, "quantity": 1, "price": 1}, timeout=5,
    )
    assert vulnerable.status_code == secure.status_code == 200
    assert "1" in vulnerable.text and "100,000" in secure.text
    assert session.get(BASE + "/vulnerable/invoice?id=1002", timeout=5).status_code == 200
    assert session.get(BASE + "/secure/invoice?id=1002", timeout=5).status_code == 403


def test_profile_tampering_pair_and_localhost_alias():
    session = login()
    vulnerable = session.post(
        BASE + "/vulnerable/profile/update",
        data={"user_id": 12, "email": "usera@lab.local", "role": "admin"}, timeout=5,
    )
    assert vulnerable.status_code == 200
    requests.post(BASE + "/reset-lab", timeout=10)
    session = login()
    secure = session.post(
        BASE + "/secure/profile/update",
        data={"user_id": 13, "email": "verified@lab.local", "role": "admin"}, timeout=5,
    )
    assert secure.status_code == 200 and "verified@lab.local" in secure.text
    assert requests.get("http://localhost:5003/health", timeout=5).status_code == 200

