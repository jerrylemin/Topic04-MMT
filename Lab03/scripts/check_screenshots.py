from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from screenshot_manifest import SCREENSHOTS  # noqa: E402


def main() -> int:
    folder = ROOT / "evidence" / "screenshots"
    required = {item["filename"] for item in SCREENSHOTS}
    actual = {path.name for path in folder.glob("*.png")}
    problems = [*(f"MISSING: {name}" for name in sorted(required - actual)), *(f"UNEXPECTED: {name}" for name in sorted(actual - required))]
    hashes: dict[str, str] = {}
    for path in sorted(folder.glob("*.png")):
        if path.stat().st_size == 0:
            problems.append(f"EMPTY: {path.name}")
            continue
        try:
            with Image.open(path) as image:
                if image.format != "PNG":
                    problems.append(f"WRONG FORMAT: {path.name}")
                if image.width < 800 or image.height < 450:
                    problems.append(f"TOO SMALL: {path.name} ({image.width}x{image.height})")
        except OSError as exc:
            problems.append(f"UNREADABLE: {path.name}: {exc}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in hashes:
            problems.append(f"DUPLICATE HASH: {path.name} and {hashes[digest]}")
        else:
            hashes[digest] = path.name
    print("\n".join(problems) if problems else f"OK: {len(required)} valid screenshots.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
