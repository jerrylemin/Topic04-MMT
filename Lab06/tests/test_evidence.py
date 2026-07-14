from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_exported_evidence_summary_is_real_and_redacted():
    summary_path = ROOT / "evidence" / "logs" / "evidence_export_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["flow_count"] == 17
    assert summary["trace_count"] == 17
    assert summary["audit_count"] >= 15
    assert summary["all_artifacts_redacted"] is True


def test_all_required_named_evidence_files_exist_and_are_nonempty():
    required_counts = {
        "traces": 17,
        "requests": 10,
        "responses": 9,
        "cookies": 9,
        "sessions": 4,
    }
    for family, minimum in required_counts.items():
        files = [path for path in (ROOT / "evidence" / family).iterdir() if path.is_file()]
        assert len(files) >= minimum
        assert all(path.stat().st_size > 0 for path in files)
