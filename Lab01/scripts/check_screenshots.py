from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import sys

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from screenshot_manifest import SCREENSHOTS, REQUIRED_FILENAMES


def inspect(folder: Path) -> dict[str, object]:
    folder.mkdir(parents=True, exist_ok=True)
    files = sorted(path for path in folder.iterdir() if path.is_file())
    expected, actual = set(REQUIRED_FILENAMES), {path.name for path in files}
    invalid: list[str] = []
    too_small: list[str] = []
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
                if width < 1024 or height < 600:
                    too_small.append(f"{path.name} ({width}x{height})")
                image.verify()
        except (OSError, UnidentifiedImageError):
            invalid.append(path.name)
            continue
        hashes.setdefault(sha256(path.read_bytes()).hexdigest(), []).append(path.name)
    return {
        "missing": sorted(expected - actual),
        "extra": sorted(actual - expected),
        "invalid": sorted(set(invalid)),
        "too_small": sorted(too_small),
        "duplicates": sorted(sorted(names) for names in hashes.values() if len(names) > 1),
        "valid_names": len(expected & actual),
    }


def main() -> int:
    parser = ArgumentParser(description="Kiểm tra tên/PNG/kích thước/hash; không OCR nội dung.")
    parser.add_argument("--directory", type=Path, default=ROOT / "evidence" / "screenshots")
    parser.add_argument("--list-required", action="store_true", help="In danh sách ảnh bắt buộc theo thứ tự.")
    args = parser.parse_args()
    if args.list_required:
        for index, item in enumerate(SCREENSHOTS, 1):
            print(f"{index:02d}. {item['filename']} - {item['purpose']}")
        return 0
    result = inspect(args.directory.resolve())
    print(f"Đúng tên: {result['valid_names']}/{len(REQUIRED_FILENAMES)}")
    for key, label in (("missing", "Thiếu"), ("extra", "Thừa"), ("invalid", "Sai PNG/rỗng/hỏng"),
                       ("too_small", "Kích thước dưới 1024x600"), ("duplicates", "Trùng SHA-256")):
        values = result[key]
        print(f"{label}: {', '.join(map(str, values)) if values else 'không'}")
    return int(any(result[key] for key in ("missing", "extra", "invalid", "too_small", "duplicates")))


if __name__ == "__main__":
    raise SystemExit(main())
