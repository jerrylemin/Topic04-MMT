@echo off
setlocal
cd /d "%~dp0\.."
if not exist .venv py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt || exit /b 1
if not exist lab04.db .venv\Scripts\python.exe seed.py || exit /b 1
echo Victim: http://127.0.0.1:5004
echo Attacker same-site: http://127.0.0.1:9004
echo Attacker cross-site: http://localhost:9004
.venv\Scripts\python.exe run_both.py
