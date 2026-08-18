"""Metadata-only checker for student-captured PNG evidence."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def check(lab_root: Path, manifest) -> int:
    folder = lab_root / "evidence" / "screenshots"
    folder.mkdir(parents=True, exist_ok=True)
    specs = tuple(manifest)
    expected = {str(item["filename"]) for item in specs}
    required = {str(item["filename"]) for item in specs if not item.get("optional", False)}
    actual_paths = tuple(path for path in folder.iterdir() if path.is_file() and path.name != ".gitkeep")
    actual = {path.name for path in actual_paths}
    invalid: list[str] = []
    too_small: list[str] = []
    hashes: dict[str, list[str]] = {}
    for path in actual_paths:
        if path.suffix.lower() != ".png" or path.stat().st_size == 0:
            invalid.append(path.name)
            continue
        try:
            with Image.open(path) as image:
                if image.format != "PNG":
                    invalid.append(path.name)
                width, height = image.size
                if width < 1024 or height < 600:
                    too_small.append(f"{path.name} ({width}x{height})")
                image.verify()
        except (OSError, UnidentifiedImageError):
            invalid.append(path.name)
            continue
        hashes.setdefault(sha256(path.read_bytes()).hexdigest(), []).append(path.name)
    duplicates = [sorted(names) for names in hashes.values() if len(names) > 1]
    missing = sorted(required - actual)
    extra = sorted(actual - expected)
    print(f"Đúng tên trong manifest: {len(actual & expected)}/{len(expected)}; bắt buộc: {len(required)}; tùy chọn: {len(expected-required)}")
    print("Thiếu bắt buộc:", ", ".join(missing) or "không")
    print("Thừa:", ", ".join(extra) or "không")
    print("PNG rỗng/hỏng:", ", ".join(sorted(set(invalid))) or "không")
    print("Ảnh quá nhỏ:", ", ".join(sorted(too_small)) or "không")
    print("Trùng SHA-256:", duplicates or "không")
    return int(bool(missing or extra or invalid or too_small or duplicates))
