"""Validate optional screenshots captured manually; never launches a browser or OCR."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "evidence" / "screenshots"
EXPECTED = (
    "01_home.png",
    "02_plain_user_denied.png",
    "03_plain_admin_manual.png",
    "04_base64_original.png",
    "05_base64_modified_manual.png",
    "06_signed_valid.png",
    "07_signed_invalid_manual.png",
    "08_encrypted_demo.png",
    "09_session_student_denied.png",
    "10_session_admin_allowed.png",
    "11_presentation_mode.png",
    "12_audit_log.png",
)


def inspect_screenshots() -> tuple[list[str], list[str]]:
    present: list[str] = []
    invalid: list[str] = []
    for name in EXPECTED:
        path = SCREENSHOTS / name
        if not path.exists():
            continue
        if not path.is_file() or path.suffix.lower() != ".png" or path.stat().st_size < 1024:
            invalid.append(name)
        else:
            present.append(name)
    return present, invalid


def main() -> int:
    present, invalid = inspect_screenshots()
    missing = [name for name in EXPECTED if name not in present and name not in invalid]
    print(f"Manual screenshots present: {len(present)}/{len(EXPECTED)}")
    if missing:
        print("Optional manual captures missing: " + ", ".join(missing))
    if invalid:
        print("Invalid or unexpectedly small PNG files: " + ", ".join(invalid))
        return 1
    print("No browser automation or OCR was executed. Screenshots are not a Codex completion gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
