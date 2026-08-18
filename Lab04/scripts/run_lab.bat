@echo off
setlocal
cd /d "%~dp0\.."
where py >nul 2>nul && (set "PYTHON=py -3.12") || (set "PYTHON=python")
%PYTHON% -m pip install --user -r requirements.txt || exit /b 1
if not exist lab04.sqlite3 %PYTHON% seed.py || exit /b 1
echo Victim: http://127.0.0.1:5004
echo Attacker same-site: http://127.0.0.1:9004
echo Attacker cross-site: http://localhost:9004
%PYTHON% run_both.py
exit /b %errorlevel%
