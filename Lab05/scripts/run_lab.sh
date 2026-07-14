#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON=${PYTHON:-python3}

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  "$PYTHON" -m venv "$ROOT/.venv"
fi

"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements.txt"
if [ ! -f "$ROOT/lab05.sqlite3" ]; then
  "$ROOT/.venv/bin/python" "$ROOT/seed.py"
fi

printf '%s\n' 'Lab05: http://127.0.0.1:5005 (Ctrl+C de dung)'
exec "$ROOT/.venv/bin/python" "$ROOT/app.py"
