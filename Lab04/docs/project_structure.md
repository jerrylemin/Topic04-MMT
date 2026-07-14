# Project structure

- `victim_app.py`, `attacker_app.py`: Flask entry points and routes.
- `*_service.py`, `trace_models.py`, `database.py`, `seed.py`: security, evidence,
  persistence, and reset behavior.
- `victim_templates/`, `attacker_templates/`, `static/`: server-rendered UI.
- `tests/`: public-behavior and submission-contract tests.
- `scripts/`: evidence export, runtime smoke, report generation, and cleanup.
- `evidence/`: named redacted runtime artefacts and verification logs.
- `report/`: final DOCX and PDF generated from source and evidence.

