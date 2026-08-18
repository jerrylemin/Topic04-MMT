# Setup and run

Windows: `python -m venv .venv`, `.venv\Scripts\activate`, `pip install -r requirements.txt`, `python seed.py`, `python app.py`.

Verify: `pytest`; demo: `python scripts/run_demo_flows.py`; report: `python scripts/generate_report.py`; screenshot check: `python scripts/check_screenshots.py`.

The app must remain bound to `127.0.0.1:5003`. `SESSION_COOKIE_SECURE=false` is for local HTTP only.

Last verified 2026-07-14: 105 tests passed, nine demo scenarios exported, and `docker compose config --quiet` passed. Docker image build still requires a running Docker Desktop Linux daemon.
