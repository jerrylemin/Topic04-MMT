@echo off
setlocal
cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" py -3.12 -m venv .venv
if errorlevel 1 exit /b 1

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
if not exist "data\lab06.sqlite3" ".venv\Scripts\python.exe" scripts\reset_database.py
if errorlevel 1 exit /b 1
echo Lab06: http://127.0.0.1:5006 (Ctrl+C to stop)
".venv\Scripts\python.exe" app.py
exit /b %errorlevel%
