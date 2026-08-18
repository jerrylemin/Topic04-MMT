import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_required_top_level_structure_exists():
    required = {
        "README.md", "requirements.txt", ".gitignore", ".env.example",
        "pytest.ini", "victim_app.py", "attacker_app.py", "run_both.py", "config.py", "database.py",
        "auth.py", "csrf_service.py", "origin_service.py", "audit_service.py", "trace_models.py",
        "trace_service.py", "security_utils.py", "schema.sql", "seed.py", "Dockerfile.victim",
        "Dockerfile.attacker", "docker-compose.yml", "scripts/generate_report.py",
        "scripts/reset_database.py", "scripts/send_legitimate_request.py", "scripts/run_runtime_smoke_test.py",
        "scripts/run_demo_flows.py", "scripts/export_evidence.py", "scripts/inspect_cookie_config.py",
        "scripts/check_origin_matrix.py", "scripts/clean_submission.py",
    }
    missing = sorted(name for name in required if not (ROOT / name).exists())
    assert not missing, f"missing required Lab04 files: {missing}"


def test_apps_and_launchers_bind_only_to_loopback():
    for name in ("victim_app.py", "attacker_app.py", "run_both.py"):
        source = (ROOT / name).read_text(encoding="utf-8")
        assert 'host="127.0.0.1"' in source
        assert 'host="0.0.0.0"' not in source


def test_dependencies_and_python_sources_exclude_browser_automation():
    requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").lower()
    assert "requests" in requirements and "pytest" in requirements
    assert "playwright" not in requirements
    assert "selenium" not in requirements
    sources = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore").lower()
        for path in ROOT.rglob("*.py")
        if "__pycache__" not in path.parts and "tests" not in path.parts
    )
    assert "import playwright" not in sources
    assert "from playwright" not in sources
    assert "import selenium" not in sources
    assert "from selenium" not in sources


def test_runtime_scripts_reject_nonlocal_victim_and_state_browser_limits():
    sender = _load("send_legitimate_request", ROOT / "scripts/send_legitimate_request.py")
    assert sender.require_local_victim("http://127.0.0.1:5004") == "http://127.0.0.1:5004"
    assert sender.require_local_victim("http://localhost:5004/") == "http://localhost:5004"
    for url in ("https://127.0.0.1:5004", "http://127.0.0.1:80", "http://example.com:5004"):
        with pytest.raises(ValueError):
            sender.require_local_victim(url)
    scripts = "\n".join(
        (ROOT / f"scripts/{name}").read_text(encoding="utf-8")
        for name in ("send_legitimate_request.py", "run_demo_flows.py", "export_evidence.py")
    )
    assert "requests.Session" in scripts
    assert "SameSite" in scripts and "SOP" in scripts
    assert "manual" in scripts


def test_origin_matrix_distinguishes_origin_from_site():
    checker = _load("check_origin_matrix", ROOT / "scripts/check_origin_matrix.py")
    rows = checker.matrix()
    assert rows[0]["same_origin"] is False and rows[0]["same_site"] is True
    assert rows[1]["same_origin"] is False and rows[1]["same_site"] is False


def test_docker_is_loopback_only_nonroot_and_not_privileged():
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    assert '"127.0.0.1:5004:5004"' in compose
    assert '"127.0.0.1:9004:9004"' in compose
    assert "network_mode: host" not in compose
    assert "privileged:" not in compose
    assert "no-new-privileges:true" in compose
    assert "cap_drop:" in compose
    for name in ("Dockerfile.victim", "Dockerfile.attacker"):
        dockerfile = (ROOT / name).read_text(encoding="utf-8")
        assert "USER labuser" in dockerfile
        assert "HEALTHCHECK" in dockerfile
    attacker_service = compose.split("  attacker:", 1)[1].split("volumes:", 1)[0]
    assert "LAB04_SECRET_KEY" not in attacker_service
    assert "lab04_database" not in attacker_service
