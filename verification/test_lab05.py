from __future__ import annotations

import requests

from conftest import local_url, require_service


BASE = local_url(5005)
BYPASS = "admin_lab' -- "
EXPANDED = "%' OR 1=1 -- "


def setup_module():
    require_service(5005)
    requests.post(BASE + "/reset-lab", timeout=10)


def test_normal_and_fixed_authentication_logic_pair():
    normal = requests.Session()
    assert normal.post(
        BASE + "/secure/login", data={"username": "admin_lab", "password": "AdminLab123!"}, timeout=10
    ).status_code == 200
    vulnerable = requests.Session().post(
        BASE + "/vulnerable/login", data={"username": BYPASS, "password": "wrong"}, timeout=10
    )
    secure = requests.Session().post(
        BASE + "/secure/login", data={"username": BYPASS, "password": "wrong"}, timeout=10
    )
    assert vulnerable.status_code == secure.status_code == 200
    assert "local_demo_bypass" in vulnerable.text
    assert "rejected" in secure.text


def test_quote_error_is_controlled_and_search_pair_differs():
    quote = requests.post(BASE + "/vulnerable/login", data={"username": "'", "password": "x"}, timeout=10)
    assert quote.status_code == 200 and "sql_syntax_error" in quote.text
    vulnerable = requests.get(BASE + "/vulnerable/search", params={"keyword": EXPANDED}, timeout=10)
    secure = requests.get(BASE + "/secure/search", params={"keyword": EXPANDED}, timeout=10)
    assert vulnerable.status_code == secure.status_code == 200
    assert "unexpected_results" in vulnerable.text
    assert "expected_results" in secure.text


def test_numeric_user_detail_and_localhost_alias():
    assert requests.get(BASE + "/secure/user", params={"id": 1}, timeout=5).status_code == 200
    assert requests.get(BASE + "/secure/user", params={"id": "1 OR 1=1"}, timeout=5).status_code == 400
    assert requests.get("http://localhost:5005/health", timeout=5).status_code == 200

