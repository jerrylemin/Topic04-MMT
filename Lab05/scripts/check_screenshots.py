"""Kiểm tra cơ học bộ ảnh thủ công; không OCR hay đánh giá nội dung."""
from __future__ import annotations
import argparse, hashlib, struct, sys, zlib
from pathlib import Path
try:
    from .screenshot_manifest import EXPECTED_FILES, SCREENSHOTS
except ImportError:
    from screenshot_manifest import EXPECTED_FILES, SCREENSHOTS

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_WIDTH, MIN_HEIGHT = 800, 450

def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != PNG_SIGNATURE: raise ValueError("sai PNG signature")
    offset, dimensions, found_iend = 8, None, False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset:offset+4])[0]
        kind, end = data[offset+4:offset+8], offset + 12 + length
        if end > len(data): raise ValueError("PNG chunk bị cắt ngắn")
        payload = data[offset+8:offset+8+length]
        crc = struct.unpack(">I", data[offset+8+length:end])[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != crc: raise ValueError("PNG chunk CRC không hợp lệ")
        if dimensions is None:
            if kind != b"IHDR" or length != 13: raise ValueError("thiếu IHDR hợp lệ")
            dimensions = struct.unpack(">II", payload[:8])
            if not all(dimensions): raise ValueError("kích thước PNG bằng 0")
        if kind == b"IEND": found_iend = True; break
        offset = end
    if dimensions is None or not found_iend: raise ValueError("PNG thiếu IEND")
    return dimensions

def validate_screenshots(directory: Path) -> list[str]:
    errors, expected = [], set(EXPECTED_FILES)
    actual = {p.name for p in directory.iterdir() if p.is_file()} if directory.is_dir() else set()
    errors += [f"THIẾU: {n}" for n in sorted(expected - actual)]
    errors += [f"THỪA: {n}" for n in sorted(actual - expected)]
    hashes: dict[str, list[str]] = {}
    for name in EXPECTED_FILES:
        path = directory / name
        if not path.is_file(): continue
        if path.stat().st_size == 0: errors.append(f"FILE RỖNG: {name}"); continue
        try: width, height = png_dimensions(path)
        except (OSError, ValueError, struct.error) as exc: errors.append(f"PNG KHÔNG HỢP LỆ: {name} ({exc})"); continue
        if width < MIN_WIDTH or height < MIN_HEIGHT: errors.append(f"KÍCH THƯỚC QUÁ NHỎ: {name} ({width}x{height}; tối thiểu {MIN_WIDTH}x{MIN_HEIGHT})")
        hashes.setdefault(hashlib.sha256(path.read_bytes()).hexdigest(), []).append(name)
    errors += [f"TRÙNG HASH: {', '.join(names)}" for names in hashes.values() if len(names) > 1]
    return errors

def main(argv=None) -> int:
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=f"Kiểm tra {len(EXPECTED_FILES)} ảnh thủ công Lab05")
    parser.add_argument("directory", nargs="?", type=Path, default=Path(__file__).resolve().parents[1]/"evidence"/"screenshots")
    parser.add_argument("--list-required", action="store_true")
    args = parser.parse_args(argv)
    if args.list_required:
        for i, item in enumerate(SCREENSHOTS, 1): print(f"{i:02d}. {item['name']} - {item['title']}")
        return 0
    errors = validate_screenshots(args.directory)
    if errors:
        print(f"Bộ ảnh chưa đạt ({len(errors)} lỗi):"); [print(f"- {e}") for e in errors]; return 1
    print(f"Đạt: đủ {len(EXPECTED_FILES)} PNG đúng tên, đủ kích thước và không trùng hash."); return 0

if __name__ == "__main__": raise SystemExit(main())
