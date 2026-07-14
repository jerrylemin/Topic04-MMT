#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
mkdir -p evidence/logs
[ ! -f .venv/bin/activate ] || . .venv/bin/activate
sh scripts/build_all.sh
python -m pytest 2>&1 | tee evidence/logs/pytest.txt
