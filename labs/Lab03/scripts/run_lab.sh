#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
[ -f lab03.db ] || python seed.py
exec python app.py
