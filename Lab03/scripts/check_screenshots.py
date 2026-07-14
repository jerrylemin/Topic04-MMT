from __future__ import annotations

import hashlib
import argparse
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from screenshot_manifest import SCREENSHOTS  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Kiểm tra ảnh thủ công của Lab03.")
    parser.add_argument("--list-required", action="store_true", help="In danh sách ảnh bắt buộc theo đúng thứ tự.")
    args = parser.parse_args()
    if args.list_required:
        for index, item in enumerate(SCREENSHOTS, 1):
            print(f"{index:02d}. {item['filename']} - {item['purpose']}")
        return 0
    folder = ROOT / "evidence" / "screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    ordered = [item["filename"] for item in SCREENSHOTS]
    required = set(ordered)
    actual_paths = [path for path in folder.iterdir() if path.is_file() and path.name != ".gitkeep"]
    actual = {path.name for path in actual_paths}
    problems = [*(f"MISSING: {name}" for name in ordered if name not in actual), *(f"UNEXPECTED: {name}" for name in sorted(actual - required))]
    hashes: dict[str, str] = {}
    for path in sorted(actual_paths):
        if path.name not in required:
            continue
        if path.suffix.lower() != ".png":
            problems.append(f"WRONG NAME/EXTENSION: {path.name}")
            continue
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
