$ErrorActionPreference='Stop'; Set-Location (Split-Path $PSScriptRoot -Parent)
if (!(Test-Path .venv)) { python -m venv .venv }
& .venv\Scripts\python -m pip install -r requirements.txt
if (!(Test-Path lab01.db)) { & .venv\Scripts\python seed.py }
& .venv\Scripts\python app.py
