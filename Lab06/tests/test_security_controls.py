from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_code_comparison_markers_are_balanced_and_unique():
    sources = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.glob("*.py"))
    starts = [line.strip() for line in sources.splitlines() if "LAB06-CODE:" in line and line.endswith(":START")]
    ends = [line.strip() for line in sources.splitlines() if "LAB06-CODE:" in line and line.endswith(":END")]
    assert starts and len(starts) == len(set(starts))
    assert len(ends) == len(set(ends)) == len(starts)
    assert {line.replace(":START", "") for line in starts} == {line.replace(":END", "") for line in ends}


def test_control_panel_template_mentions_control_limitations():
    source = (ROOT / "templates" / "components" / "security_controls.html").read_text(encoding="utf-8").lower()
    assert "httponly" in source and "samesite" in source
    assert "giới hạn" in source or "limit" in source


def test_base64_is_not_described_as_encryption_in_inspector():
    source = (ROOT / "templates" / "components" / "base64_inspector.html").read_text(encoding="utf-8").lower()
    assert "not encryption" in source or "không" in source


def test_encryption_inspector_states_authorization_is_separate():
    source = (ROOT / "templates" / "components" / "encryption_inspector.html").read_text(encoding="utf-8").lower()
    assert "authorization" in source or "phân quyền" in source


def test_security_controls_are_derived_from_runtime_route(client):
    response = client.get("/security-controls")
    assert response.status_code == 200
    assert "CSP" in response.get_data(as_text=True)

