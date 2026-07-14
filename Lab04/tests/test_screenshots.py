import subprocess
import sys
from pathlib import Path

from screenshot_manifest import SCREENSHOTS

ROOT = Path(__file__).resolve().parents[1]


def test_guide_and_manifest_use_seven_images():
    guide = (ROOT / "HUONG_DAN_CHUP_ANH.md").read_text(encoding="utf-8")
    assert len(SCREENSHOTS) == 7
    assert all(item["filename"] in guide for item in SCREENSHOTS)
    assert all(f"Bước {number}." in guide for number in range(1, 7))


def test_checker_lists_images_in_manifest_order():
    result = subprocess.run([sys.executable, "scripts/check_screenshots.py", "--list-required"], cwd=ROOT,
                            text=True, encoding="utf-8", capture_output=True, check=True)
    listed = [line.split(" - ", 1)[0][4:] for line in result.stdout.splitlines()]
    assert listed == [item["filename"] for item in SCREENSHOTS]
