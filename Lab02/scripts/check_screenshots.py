from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path

from PIL import Image, UnidentifiedImageError


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = (
    "01_home_overview.png",
    "02_normal_input_before_submit.png",
    "03_normal_http_request.png",
    "04_normal_native_process.png",
    "05_normal_memory_visualizer.png",
    "06_overflow_32_input.png",
    "07_overflow_32_memory_boundary.png",
    "08_overflow_64_request.png",
    "09_overflow_64_strcpy_step.png",
    "10_overflow_64_memory_visualizer.png",
    "11_asan_detected.png",
    "12_asan_stack_trace.png",
    "13_native_crash_result.png",
    "14_final_vulnerable_verdict.png",
    "15_length_test_table.png",
    "16_gdb_breakpoint.png",
    "17_gdb_local_buffer.png",
    "18_gdb_overflow_stop.png",
    "19_secure_length_reject.png",
    "20_secure_length_timeline.png",
    "21_secure_snprintf_reject.png",
    "22_code_comparison.png",
    "23_hardening_comparison.png",
    "24_stack_canary_explanation.png",
    "25_asan_vs_hardening.png",
    "26_presentation_mode.png",
    "27_pytest_passed.png",
    "28_report_files.png",
)


def inspect(folder: Path) -> dict[str, object]:
    folder.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in folder.iterdir() if path.is_file())
    expected, actual = set(EXPECTED), {path.name for path in files}
    invalid: list[str] = []
    unreasonable: list[str] = []
    hashes: dict[str, list[str]] = {}

    for path in files:
        if path.suffix.lower() != ".png" or path.stat().st_size == 0:
            invalid.append(path.name)
            continue
        try:
            with Image.open(path) as image:
                if image.format != "PNG":
                    invalid.append(path.name)
                width, height = image.size
                if width < 1024 or height < 600 or width > 16_384 or height > 16_384:
                    unreasonable.append(f"{path.name} ({width}x{height})")
                image.verify()
        except (OSError, UnidentifiedImageError):
            invalid.append(path.name)
            continue
        digest = sha256(path.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(path.name)

    return {
        "missing": sorted(expected - actual),
        "extra": sorted(actual - expected),
        "invalid": sorted(set(invalid)),
        "unreasonable": sorted(unreasonable),
        "duplicates": sorted(sorted(names) for names in hashes.values() if len(names) > 1),
        "valid_names": len(expected & actual),
    }


def main() -> int:
    parser = ArgumentParser(description="Kiểm tra file PNG, kích thước và hash; không OCR nội dung.")
    parser.add_argument("--directory", type=Path, default=ROOT / "evidence" / "screenshots")
    result = inspect(parser.parse_args().directory.resolve())
    print(f"Đúng tên: {result['valid_names']}/{len(EXPECTED)}")
    for key, label in (
        ("missing", "Thiếu"),
        ("extra", "Thừa"),
        ("invalid", "Sai PNG/rỗng/hỏng"),
        ("unreasonable", "Kích thước không hợp lý"),
        ("duplicates", "Trùng SHA-256"),
    ):
        values = result[key]
        print(f"{label}: {', '.join(map(str, values)) if values else 'không'}")
    return int(any(result[key] for key in ("missing", "extra", "invalid", "unreasonable", "duplicates")))


if __name__ == "__main__":
    raise SystemExit(main())
