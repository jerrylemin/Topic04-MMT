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
    files = sorted(p for p in folder.iterdir() if p.is_file())
    expected, actual = set(REQUIRED_FILENAMES), {p.name for p in files}
    invalid, too_small, hashes = [], [], {}
    for path in files:
        if path.suffix.lower() != ".png" or path.stat().st_size == 0:
            invalid.append(path.name); continue
        try:
            with Image.open(path) as image:
                if image.format != "PNG": invalid.append(path.name)
                if image.width < 1024 or image.height < 600: too_small.append(f"{path.name} ({image.width}x{image.height})")
                image.verify()
        except (OSError, UnidentifiedImageError):
            invalid.append(path.name); continue
        hashes.setdefault(sha256(path.read_bytes()).hexdigest(), []).append(path.name)
    return {"missing":sorted(expected-actual),"extra":sorted(actual-expected),"invalid":sorted(set(invalid)),
            "too_small":sorted(too_small),"duplicates":sorted(sorted(v) for v in hashes.values() if len(v)>1),"valid_names":len(expected&actual)}

def main() -> int:
    parser=ArgumentParser(description="Kiểm tra tên/PNG/kích thước/hash; không OCR nội dung.")
    parser.add_argument("--directory",type=Path,default=ROOT/"evidence/screenshots")
    parser.add_argument("--list-required",action="store_true")
    args=parser.parse_args()
    if args.list_required:
        for i,item in enumerate(SCREENSHOTS,1): print(f"{i:02d}. {item['filename']} - {item['purpose']}")
        return 0
    result=inspect(args.directory.resolve()); print(f"Đúng tên: {result['valid_names']}/{len(REQUIRED_FILENAMES)}")
    for key,label in (("missing","Thiếu"),("extra","Thừa"),("invalid","Sai PNG/rỗng/hỏng"),("too_small","Kích thước dưới 1024x600"),("duplicates","Trùng SHA-256")):
        values=result[key]; print(f"{label}: {', '.join(map(str,values)) if values else 'không'}")
    return int(any(result[k] for k in ("missing","extra","invalid","too_small","duplicates")))

if __name__ == "__main__": raise SystemExit(main())
