from pathlib import Path

from attacker_app import create_app


ROOT = Path(__file__).resolve().parents[1]


def test_attacker_home_health_and_local_security_headers():
    client = create_app({"TESTING": True}).test_client()
    assert client.get("/").status_code == 200
    health = client.get("/health")
    assert health.status_code == 200
    assert health.get_json()["service"] == "demo-page"
    csp = client.get("/").headers["Content-Security-Policy"]
    assert "form-action 'self' http://127.0.0.1:5004" in csp
    assert "connect-src 'self'" in csp
    assert "https:" not in csp


def test_attack_routes_render_only_local_forms_with_expected_token_behavior():
    client = create_app({"TESTING": True}).test_client()
    cases = {
        "/attack/vulnerable-email": (b"/vulnerable/change-email", False),
        "/attack/secure-email": (b"/secure/change-email", False),
        "/attack/bad-token": (b"/secure/change-email", True),
    }
    for route, (target, has_token) in cases.items():
        response = client.get(route)
        assert response.status_code == 200
        assert b'method="POST"' in response.data
        assert b'action="http://127.0.0.1:5004' + target + b'"' in response.data
        assert (b'name="csrf_token"' in response.data) is has_token
        assert b"https://" not in response.data


def test_attacker_code_does_not_read_cookies_or_use_browser_automation():
    executable = "\n".join(
        path.read_text(encoding="utf-8")
        for folder in (ROOT / "static/attacker/js",)
        for path in folder.glob("*.js")
    ).lower()
    assert "document.cookie" not in executable
    assert "fetch(" not in executable
    assert "xmlhttprequest" not in executable
    assert "playwright" not in executable
    assert "selenium" not in executable


def test_demo_requires_a_click_and_has_no_iframe_or_sensitive_cross_origin_flow():
    client = create_app({"TESTING": True}).test_client()
    assert client.get("/attack/password").status_code == 404
    assert client.get("/attack/transfer").status_code == 404
    assert client.get("/attack/unsafe-get").status_code == 404

    rendered = client.get("/attack/vulnerable-email").get_data(as_text=True).lower()
    source = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for folder in (ROOT / "attacker_templates", ROOT / "static/attacker/js")
        for path in folder.glob("**/*")
        if path.is_file()
    )
    for forbidden in (
        "auto_submit",
        "auto-submit",
        "form.submit",
        "<iframe",
        "contentdocument",
        "data-victim-frame",
    ):
        assert forbidden not in source
        assert forbidden not in rendered
    assert 'type="submit"' in rendered
    assert "confirm(" in source


def test_origin_demo_labels_expected_and_observed_instead_of_faking_browser_results():
    response = create_app({"TESTING": True}).test_client().get("/origin-demo")
    assert response.status_code == 200
    assert b"Expected" in response.data
    assert b"Observed" in response.data
    assert b"Not Observable" in response.data
