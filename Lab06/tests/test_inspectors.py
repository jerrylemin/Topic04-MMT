from __future__ import annotations

from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "templates" / "components"


@pytest.mark.parametrize(
    "filename",
    [
        "cookie_inspector.html",
        "cookie_attribute_inspector.html",
        "cookie_diff_inspector.html",
        "base64_inspector.html",
        "signature_inspector.html",
        "encryption_inspector.html",
        "server_session_inspector.html",
        "authorization_inspector.html",
        "database_inspector.html",
        "audit_inspector.html",
        "final_verdict.html",
        "trace_panel.html",
    ],
)
def test_required_inspector_component_exists(filename):
    path = COMPONENTS / filename
    assert path.is_file() and path.read_text(encoding="utf-8").strip()


def test_dashboard_is_available(client):
    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Plain Cookie" in body and "Server Session" in body


def test_comparison_route_renders_live_code_comparison(client):
    response = client.get("/comparison")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Code Comparison" in body
    assert "plain_authorization" in body or "lab06_role" in body


def test_security_controls_route_is_available(client):
    response = client.get("/security-controls")
    assert response.status_code == 200
    assert "Security Control" in response.get_data(as_text=True)


def test_inspector_templates_never_render_known_secret_field_names():
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in COMPONENTS.glob("*.html"))
    assert "fernet_key" not in combined
    assert "signing_key" not in combined
    assert "password_hash" not in combined


def test_static_trace_ui_only_exports_loaded_trace():
    source = (ROOT / "static" / "js" / "trace-ui.js").read_text(encoding="utf-8")
    assert "JSON.stringify(trace" in source
    assert "document.cookie" not in source


def test_presentation_script_does_not_modify_cookies():
    source = (ROOT / "static" / "js" / "presentation.js").read_text(encoding="utf-8")
    assert "document.cookie" not in source
    assert "set_cookie" not in source.lower()

