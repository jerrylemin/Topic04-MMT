@echo off
setlocal
cd /d "%~dp0.."
where py >nul 2>nul && (set "PYTHON=py -3.12") || (set "PYTHON=python")
%PYTHON% -m pip install --user -r requirements.txt || exit /b 1
if not exist lab05.sqlite3 %PYTHON% seed.py || exit /b 1
echo Lab05: http://127.0.0.1:5005 (Ctrl+C to stop)
%PYTHON% app.py
exit /b %errorlevel%
