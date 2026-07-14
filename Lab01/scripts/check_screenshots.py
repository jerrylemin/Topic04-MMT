from hashlib import sha256
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))
from screenshot_manifest import SCREENSHOTS

ROOT = Path(__file__).parents[1]
folder = ROOT / "evidence/screenshots"
folder.mkdir(parents=True, exist_ok=True)
expected = {name for name, *_ in SCREENSHOTS}
actual = {path.name for path in folder.iterdir() if path.is_file()}
missing, extra = sorted(expected - actual), sorted(actual - expected)
invalid, small, hashes = [], [], {}
for path in folder.iterdir():
    if not path.is_file(): continue
    if path.suffix.lower() != ".png" or path.stat().st_size == 0: invalid.append(path.name)
    if 0 < path.stat().st_size < 10_000: small.append(path.name)
    digest = sha256(path.read_bytes()).hexdigest(); hashes.setdefault(digest, []).append(path.name)
duplicates = [names for names in hashes.values() if len(names) > 1]
print(f"Ảnh hợp lệ theo tên: {len(actual & expected)}/28")
print("Thiếu:", ", ".join(missing) or "không")
print("Thừa:", ", ".join(extra) or "không")
print("Sai định dạng/rỗng:", ", ".join(invalid) or "không")
print("Quá nhỏ (<10 KB):", ", ".join(small) or "không")
print("Trùng hash:", duplicates or "không")
raise SystemExit(1 if missing or extra or invalid or small or duplicates else 0)
