import pytest


@pytest.mark.parametrize("path", ["/", "/vulnerable/login", "/secure/login", "/health"])
def test_all_representative_routes_send_required_headers(shared_client, path):
    response = shared_client.get(path)
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert "Permissions-Policy" in response.headers
    assert "Content-Security-Policy" in response.headers


def test_csp_has_no_unsafe_eval_or_external_wildcard(shared_client):
    csp = shared_client.get("/").headers["Content-Security-Policy"]
    assert "unsafe-eval" not in csp
    assert "*" not in csp
    assert "frame-ancestors 'none'" in csp


@pytest.mark.parametrize("path", ["/vulnerable/login", "/secure/login", "/logout"])
def test_authentication_pages_disable_cache(shared_client, path):
    response = shared_client.get(path) if path != "/logout" else shared_client.post(path)
    assert response.headers["Cache-Control"] == "no-store"


def test_session_cookie_security_defaults(shared_app):
    assert shared_app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert shared_app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert shared_app.config["SESSION_COOKIE_SECURE"] is False

