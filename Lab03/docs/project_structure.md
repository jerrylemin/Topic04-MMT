# Project structure

- `app.py`: Flask routes and headers.
- `services.py`: product/cart and the three vulnerable/secure pairs.
- `database.py`, `schema.sql`, `seed.py`: SQLite lifecycle and fixtures.
- `auth.py`, `authorization.py`, `validators.py`: identity and policy.
- `audit_service.py`, `trace_models.py`, `trace_service.py`: evidence pipeline.
- `templates/`, `static/`: UI, inspectors, timeline and Presentation Mode.
- `scripts/`: run/reset/demo/export/check/report utilities.
- `tests/`: behavior and safety regressions.
- `evidence/`: real generated traces, requests, responses, logs, database and manual screenshots.
- `report/`: final DOCX/PDF.
