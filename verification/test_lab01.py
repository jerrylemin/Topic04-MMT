from __future__ import annotations

import requests

from conftest import local_url, require_service


BASE = local_url(5000)
PAYLOAD = '<img src=x onerror="alert(\'XSS\')">'


def setup_module():
    require_service(5000, "/")
    requests.post(BASE + "/vulnerable/post/1/comments", data={"action": "clear"}, timeout=5)


def test_reflected_xss_vulnerable_and_secure_pair():
    vulnerable = requests.get(BASE + "/vulnerable/search", params={"q": PAYLOAD}, timeout=5)
    secure = requests.get(BASE + "/secure/search", params={"q": PAYLOAD}, timeout=5)
    assert vulnerable.status_code == secure.status_code == 200
    assert PAYLOAD in vulnerable.text
    assert "&lt;img" in secure.text and PAYLOAD not in secure.text
    assert "Content-Security-Policy" in secure.headers


def test_stored_xss_persists_but_secure_render_sanitizes():
    created = requests.post(
        BASE + "/vulnerable/post/1/comments",
        data={"author": "Verifier", "body": PAYLOAD},
        timeout=5,
    )
    secure = requests.get(BASE + "/secure/post/1/comments", timeout=5)
    assert created.status_code == secure.status_code == 200
    assert PAYLOAD in created.text
    assert "onerror" not in secure.text.split("Dữ liệu gốc trong DB", 1)[0]


def test_dom_sources_use_expected_sink_and_local_hosts_work():
    vulnerable = requests.get(BASE + "/static/js/dom_vulnerable.js", timeout=5)
    secure = requests.get(BASE + "/static/js/dom_secure.js", timeout=5)
    assert "innerHTML" in vulnerable.text and "textContent" in secure.text
    assert requests.get("http://localhost:5000/", timeout=5).status_code == 200

