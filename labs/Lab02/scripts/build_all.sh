#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

for tool in gcc make; do
    command -v "$tool" >/dev/null 2>&1 || {
        echo "Thiếu $tool. Hãy chạy trong Ubuntu/WSL hoặc Docker." >&2
        exit 1
    }
done

make all
echo "Đã build 5 binary trong $ROOT/build"
