from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_manual_screenshot_guide_has_exactly_48_numbered_entries():
    text = (ROOT / "HUONG_DAN_CHUP_ANH.md").read_text(encoding="utf-8")
    entries = re.findall(r"^###\s+\d{2}\.\s+`[^`]+\.png`", text, re.MULTILINE)
    assert len(entries) == 48
    assert "document.cookie" in text
    assert "completion gate" in text
