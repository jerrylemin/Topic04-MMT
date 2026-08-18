#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
[ -f lab04.db ] || python seed.py
printf '%s\n' 'Victim: http://127.0.0.1:5004' 'Attacker same-site: http://127.0.0.1:9004' 'Attacker cross-site: http://localhost:9004'
exec python run_both.py
