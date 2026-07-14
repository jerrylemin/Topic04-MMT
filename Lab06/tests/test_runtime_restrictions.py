from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _production_sources():
    return [path for path in ROOT.glob("*.py") if path.name != "seed.py"]


def test_app_rejects_non_local_host_header(client):
    response = client.get("/", headers={"Host": "example.com"})
    assert response.status_code == 400


def test_app_accepts_only_configured_local_host(client):
    assert client.get("/", headers={"Host": "127.0.0.1:5006"}).status_code == 200
    assert client.get("/", headers={"Host": "localhost:5006"}).status_code == 200


def test_runtime_host_port_and_debug_are_fixed():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'HOST = "127.0.0.1"' in source
    assert "PORT = 5006" in source
    assert "run(host=HOST, port=PORT, debug=False)" in source
    assert "0.0.0.0" not in source


def test_runtime_source_does_not_import_network_clients():
    forbidden = {"requests", "urllib", "httpx", "socket", "aiohttp"}
    for path in _production_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        assert forbidden.isdisjoint(imported), f"network client imported by {path.name}: {forbidden & imported}"


def test_javascript_never_reads_or_writes_browser_cookies():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "static" / "js").glob("*.js"))
    assert "document.cookie" not in combined


def test_source_has_no_browser_automation_dependency():
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in ROOT.rglob("*.py") if "tests" not in path.parts)
    assert "playwright" not in combined and "selenium" not in combined


def test_login_rejects_unlisted_mode(client):
    response = client.post(
        "/login",
        data={"username": "student", "password": "Student123!", "mode": "custom"},
    )
    assert response.status_code == 400


def test_oversized_login_body_is_rejected(client, app):
    response = client.post(
        "/login",
        data={"username": "student", "password": "x" * (app.config["MAX_CONTENT_LENGTH"] + 1), "mode": "plain"},
    )
    assert response.status_code == 413


def test_state_changing_endpoints_reject_get(client):
    assert client.get("/logout").status_code == 405
    assert client.get("/secure/session/logout").status_code == 405


def test_login_form_has_no_arbitrary_target_fields(client):
    body = client.get("/login").get_data(as_text=True).lower()
    for forbidden_name in ('name="host"', 'name="url"', 'name="port"', 'name="cookie_name"', 'name="target_route"'):
        assert forbidden_name not in body
