from __future__ import annotations

from flask import Response

from config import cookie_options
from cookie_service import issue_plain_demo_cookies
from encrypted_cookie_service import issue_encrypted_demo_cookie
from server_session_service import SessionIssue, set_session_cookie
from signed_cookie_service import issue_signed_cookie


def test_cookie_options_are_host_only_lax_and_root_scoped(app):
    options = cookie_options(app.config, httponly=True)
    assert options == {"path": "/", "secure": False, "httponly": True, "samesite": "Lax"}
    assert "domain" not in options


def test_plain_demo_cookie_is_observable_but_not_secure_authorization(app):
    response = Response()
    issue_plain_demo_cookies(response, app.config)
    assert all("HttpOnly" not in item for item in response.headers.getlist("Set-Cookie"))


def test_signed_cookie_is_httponly(app):
    response = Response()
    issue_signed_cookie(response, "masked-demo-token", app.config)
    assert "HttpOnly" in response.headers["Set-Cookie"]


def test_encrypted_cookie_is_httponly(app):
    response = Response()
    issue_encrypted_demo_cookie(response, "masked-demo-token", app.config)
    assert "HttpOnly" in response.headers["Set-Cookie"]


def test_session_cookie_has_expiry_and_httponly(app):
    issue = SessionIssue(10, "opaque-token", "fingerprint", "now", "later", "login")
    response = Response()
    set_session_cookie(response, issue, app.config)
    header = response.headers["Set-Cookie"]
    assert "HttpOnly" in header and "SameSite=Lax" in header and "Max-Age=1800" in header


def test_secure_flag_follows_configuration(app):
    app.config["COOKIE_SECURE"] = True
    response = Response()
    issue_signed_cookie(response, "masked-demo-token", app.config)
    assert "Secure" in response.headers["Set-Cookie"]
