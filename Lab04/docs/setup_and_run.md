# Setup and run

Use the existing virtual environment: `./.venv/Scripts/python.exe run_both.py`.
Open the fixed loopback ports 5004 and 9004. Run the suite with
`py -3.12 -m pytest -q`; run the live loopback checks with
`./.venv/Scripts/python.exe scripts/run_runtime_smoke_test.py` while both apps are
running. Generate evidence before the report, then run `scripts/clean_submission.py`.
See `README.md` for credentials and exact workflows.

