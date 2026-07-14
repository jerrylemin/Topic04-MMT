#!/usr/bin/env sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
if [ ! -f data/lab06.sqlite3 ]; then
  .venv/bin/python scripts/reset_database.py
fi
echo "Lab06: http://127.0.0.1:5006 (Ctrl+C to stop)"
exec .venv/bin/python app.py
