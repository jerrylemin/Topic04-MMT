#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

if [ "$(id -u)" -eq 0 ]; then
    echo "Không chạy lab bằng root. Hãy dùng user thường trong Linux/WSL hoặc service web của Docker." >&2
    exit 1
fi
for tool in python3 gcc make; do
    command -v "$tool" >/dev/null 2>&1 || {
        echo "Thiếu $tool. Trên Windows hãy dùng WSL hoặc Docker." >&2
        exit 1
    }
done

[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
sh scripts/build_all.sh
echo "Mở http://127.0.0.1:5002 - dừng bằng Ctrl+C"
exec python app.py
