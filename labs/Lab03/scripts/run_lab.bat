@echo off
setlocal
cd /d "%~dp0.."
if not exist .venv python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt || exit /b 1
if not exist lab03.db .venv\Scripts\python.exe seed.py || exit /b 1
.venv\Scripts\python.exe app.py
