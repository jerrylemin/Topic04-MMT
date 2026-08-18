@echo off
setlocal
cd /d "%~dp0.."

where py >nul 2>nul && (set "PYTHON=py -3.12") || (set "PYTHON=python")
%PYTHON% -m pip install --user -r requirements.txt || exit /b 1
echo Lab06: http://127.0.0.1:5006 (Ctrl+C to stop)
%PYTHON% app.py
exit /b %errorlevel%
