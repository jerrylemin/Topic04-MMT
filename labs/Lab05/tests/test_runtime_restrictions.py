import re
from pathlib import Path

import pytest

from config import FIXED_TEST_INPUTS, SERVER_HOST, SERVER_PORT


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_bind_is_fixed_loopback_only():
    assert SERVER_HOST == "127.0.0.1"
    assert SERVER_PORT == 5005
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'host="127.0.0.1"' in app_source
    assert "0.0.0.0" not in app_source


@pytest.mark.parametrize("dependency", ["playwright", "selenium", "sqlmap"])
def test_requirements_exclude_scanners_and_browser_automation(dependency):
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
    assert dependency not in requirements


@pytest.mark.parametrize("term", [
    "union select", "sqlite_master", "attach database", "load_extension",
    "pragma", " drop ", " alter ", " insert ", " update ", " delete ",
])
def test_vulnerable_query_module_has_no_out_of_scope_operation(term):
    source = f" {(ROOT / 'vulnerable_queries.py').read_text(encoding='utf-8').lower()} "
    assert term not in source


@pytest.mark.parametrize("name", ["host", "url", "port", "database", "sql", "connection_string"])
def test_templates_do_not_offer_target_or_raw_sql_input(name):
    templates = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "templates").rglob("*.html"))
    assert not re.search(rf'<(?:input|textarea|select)[^>]+name=["\']{name}["\']', templates, re.IGNORECASE)


def test_fixed_test_inputs_are_small_named_scenarios_not_user_targets():
    assert set(FIXED_TEST_INPUTS) == {
        "normal_login", "quote", "authentication_logic", "normal_search", "expanded_search"
    }
    serialized = " ".join(FIXED_TEST_INPUTS.values()).lower()
    assert "http://" not in serialized and "https://" not in serialized


def test_compose_publishes_only_loopback_port():
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    assert '"127.0.0.1:5005:5005"' in compose
    assert "privileged:" not in compose
    assert "no-new-privileges:true" in compose


def test_docker_runs_as_non_root_user():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "USER labuser" in dockerfile
    assert "USER root" not in dockerfile


def test_application_core_has_no_network_client_import():
    core = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in ("app.py", "database.py", "auth_service.py", "vulnerable_queries.py", "secure_queries.py")
    )
    assert "import requests" not in core
    assert "urllib.request" not in core
    assert "http.client" not in core


def test_flask_debug_is_disabled(shared_app):
    assert shared_app.debug is False

