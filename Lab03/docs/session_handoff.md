# Session handoff

Lab03 Parameter Tampering is implemented and verified. The Flask app stays on `127.0.0.1:5003`, uses fixed simulated data, and provides vulnerable/secure checkout price tampering, invoice IDOR, and role mass-assignment flows with real SQLite audit/trace records, inspectors, comparisons, and Presentation Mode.

Final evidence on 2026-07-14:

- `python -m pytest`: 105 passed in 14.36s; exact output is in `evidence/logs/pytest.txt`.
- `scripts/run_demo_flows.py`: all 9 scenarios completed with expected outcomes; trace IDs are unique.
- `PRAGMA integrity_check`: `ok`; exported database has 13 audit events across six action types.
- Python compile, all JavaScript syntax checks, primary route smoke tests, and `docker compose config --quiet` passed.
- A real local HTTP runtime was exercised for the vulnerable checkout, secure IDOR 403, and secure profile scenarios, then stopped.
- Final report artifacts open structurally, contain `105 passed`, and the PDF has 50 A4 pages; the rendered final page was visually checked.

Remaining operator action: capture the 41 manual PNGs listed in `HUONG_DAN_CHUP_ANH.md` into `evidence/screenshots/`, run `python scripts/check_screenshots.py`, then rerun `python scripts/generate_report.py`. Browser automation is intentionally prohibited. Docker image build could not be executed because the local Docker Desktop Linux daemon was not running; Compose parsing itself passed.
