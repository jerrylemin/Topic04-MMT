from argparse import ArgumentParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = [
    *(ROOT / "build").glob("vulnerable_*"),
    *(ROOT / "build").glob("secure_*"),
    *(ROOT / "report").glob("21127645_LeMinh_Lab02_BufferOverflow.*"),
]
DIRECTORIES = [
    ROOT / "evidence" / name
    for name in ("asan", "binaries", "gdb", "logs", "requests", "responses", "snippets", "traces")
]


def candidates() -> list[Path]:
    files = list(FILES)
    for directory in DIRECTORIES:
        if directory.exists():
            files.extend(path for path in directory.rglob("*") if path.is_file())
    return sorted(set(files))


def main() -> int:
    parser = ArgumentParser(description="Dọn file sinh ra; không đụng evidence/screenshots.")
    parser.add_argument("--yes", action="store_true", help="Xóa thật; mặc định chỉ liệt kê.")
    args = parser.parse_args()
    files = candidates()
    for path in files:
        print(path.relative_to(ROOT))
        if args.yes:
            path.unlink(missing_ok=True)
    print(f"{'Đã xóa' if args.yes else 'Sẽ xóa'} {len(files)} file.")
    if not args.yes:
        print("Chạy lại với --yes để xác nhận. Ảnh chụp thủ công luôn được giữ lại.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
