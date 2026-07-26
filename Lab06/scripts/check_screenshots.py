from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "scripts"))
from screenshot_manifest import ALL_SCREENSHOTS
from screenshot_checker import check

if __name__ == "__main__":
    raise SystemExit(check(ROOT, ALL_SCREENSHOTS))
