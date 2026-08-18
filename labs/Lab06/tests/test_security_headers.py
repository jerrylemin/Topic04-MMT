from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "DENY"),
        ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ],
)
def test_core_security_header_values(client, header, expected):
    assert client.get("/").headers[header] == expected


def test_csp_has_no_unsafe_eval_or_wildcard(client):
    csp = client.get("/").headers["Content-Security-Policy"]
    assert "unsafe-eval" not in csp
    assert "*" not in csp
    assert "object-src 'none'" in csp and "frame-ancestors 'none'" in csp


def test_permissions_policy_disables_sensitive_capabilities(client):
    policy = client.get("/").headers["Permissions-Policy"]
    for capability in ("camera=()", "microphone=()", "geolocation=()", "payment=()"):
        assert capability in policy


@pytest.mark.parametrize("path", ["/login", "/vulnerable/plain/admin", "/secure/session/admin"])
def test_sensitive_pages_disable_caching(client, path):
    response = client.get(path)
    assert "no-store" in response.headers["Cache-Control"]


def test_responses_do_not_enable_wildcard_cors(client):
    response = client.get("/")
    assert response.headers.get("Access-Control-Allow-Origin") != "*"

