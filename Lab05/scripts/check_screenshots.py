"""Validate the manually captured screenshot set without inspecting its content."""

from __future__ import annotations

import argparse
import hashlib
import struct
import zlib
from pathlib import Path


EXPECTED_FILES = (
    "01_home_overview.png",
    "02_database_seed.png",
    "03_vulnerable_login_normal.png",
    "04_vulnerable_login_request.png",
    "05_vulnerable_login_query.png",
    "06_quote_login_input.png",
    "07_quote_login_error.png",
    "08_auth_logic_input.png",
    "09_auth_query_changed.png",
    "10_auth_decision_vulnerable.png",
    "11_auth_session_created.png",
    "12_secure_login_same_input.png",
    "13_secure_login_parameter_binding.png",
    "14_secure_login_rejected.png",
    "15_secure_login_normal_success.png",
    "16_vulnerable_search_normal.png",
    "17_vulnerable_search_query.png",
    "18_quote_search_error.png",
    "19_expanded_search_input.png",
    "20_expanded_search_query.png",
    "21_expanded_search_results.png",
    "22_secure_search_same_input.png",
    "23_secure_search_binding.png",
    "24_secure_search_expected_results.png",
    "25_query_visualizer.png",
    "26_code_comparison_login.png",
    "27_code_comparison_search.png",
    "28_error_comparison.png",
    "29_password_hashing.png",
    "30_security_controls.png",
    "31_audit_logs.png",
    "32_trace_timeline.png",
    "33_presentation_mode.png",
    "34_pytest_passed.png",
    "35_coverage.png",
    "36_report_files.png",
)

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MIN_WIDTH = 800
MIN_HEIGHT = 450


def png_dimensions(path: Path) -> tuple[int, int]:
    """Validate the PNG chunk structure and return dimensions from IHDR."""
    data = path.read_bytes()
    if len(data) < 33 or data[:8] != PNG_SIGNATURE:
        raise ValueError("sai PNG signature")
    offset = 8
    dimensions = None
    found_iend = False
    while offset + 12 <= len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            raise ValueError("PNG chunk bị cắt ngắn")
        payload = data[offset + 8 : offset + 8 + length]
        stored_crc = struct.unpack(">I", data[offset + 8 + length : chunk_end])[0]
        if zlib.crc32(chunk_type + payload) & 0xFFFFFFFF != stored_crc:
            raise ValueError("PNG chunk CRC không hợp lệ")
        if dimensions is None:
            if chunk_type != b"IHDR" or length != 13:
                raise ValueError("thiếu IHDR hợp lệ")
            dimensions = struct.unpack(">II", payload[:8])
            if not all(dimensions):
                raise ValueError("kích thước PNG bằng 0")
        if chunk_type == b"IEND":
            found_iend = True
            break
        offset = chunk_end
    if dimensions is None or not found_iend:
        raise ValueError("PNG thiếu IEND")
    return dimensions


def validate_screenshots(directory: Path) -> list[str]:
    errors: list[str] = []
    expected = set(EXPECTED_FILES)
    actual = {path.name for path in directory.iterdir() if path.is_file()} if directory.is_dir() else set()

    for name in sorted(expected - actual):
        errors.append(f"THIẾU: {name}")
    for name in sorted(actual - expected):
        errors.append(f"THỪA: {name}")

    hashes: dict[str, list[str]] = {}
    for name in EXPECTED_FILES:
        path = directory / name
        if not path.is_file():
            continue
        if path.suffix != ".png":
            errors.append(f"SAI ĐỊNH DẠNG: {name}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"FILE RỖNG: {name}")
            continue
        try:
            width, height = png_dimensions(path)
        except (OSError, ValueError, struct.error) as exc:
            errors.append(f"PNG KHÔNG HỢP LỆ: {name} ({exc})")
            continue
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            errors.append(
                f"KÍCH THƯỚC QUÁ NHỎ: {name} ({width}x{height}; tối thiểu {MIN_WIDTH}x{MIN_HEIGHT})"
            )
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(name)

    for names in hashes.values():
        if len(names) > 1:
            errors.append(f"TRÙNG HASH: {', '.join(names)}")
    return errors


def main() -> int:
    default_dir = Path(__file__).resolve().parents[1] / "evidence" / "screenshots"
    parser = argparse.ArgumentParser(description="Kiểm tra 36 ảnh chụp thủ công của LAB 5.")
    parser.add_argument("directory", nargs="?", type=Path, default=default_dir)
    args = parser.parse_args()

    errors = validate_screenshots(args.directory)
    if errors:
        print(f"Bộ ảnh chưa đạt ({len(errors)} lỗi):")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Đạt: đủ {len(EXPECTED_FILES)} ảnh PNG, đúng tên/kích thước và không trùng hash.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
