from __future__ import annotations

import re
from pathlib import Path

from screenshot_manifest import ALL_SCREENSHOTS, F12_SCREENSHOTS, OPTIONAL_SCREENSHOT_NAMES


ROOT = Path(__file__).resolve().parents[1]


def test_manual_screenshot_guide_covers_manifest_entries():
    text = (ROOT / "HUONG_DAN_CHUP_ANH.md").read_text(encoding="utf-8")
    entries = re.findall(r"^###\s+\d{2}\.\s+`[^`]+\.png`", text, re.MULTILINE)
    assert len(entries) == 48 - len(OPTIONAL_SCREENSHOT_NAMES)
    assert len(ALL_SCREENSHOTS) == 60
    assert all(item["filename"] in text for item in F12_SCREENSHOTS)
    assert "document.cookie" in text
    assert "python scripts/check_screenshots.py" in text
    assert "không chụp hoặc tạo ảnh" in text
