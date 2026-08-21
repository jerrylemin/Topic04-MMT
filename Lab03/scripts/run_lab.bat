@echo off
setlocal
cd /d "%~dp0.."

set "PYTHON="
where py >nul 2>nul
if not errorlevel 1 py -3 -c "import sys; raise SystemExit(0 if sys.version_info[0] == 3 else 1)" >nul 2>nul
if not errorlevel 1 set "PYTHON=py -3"

if not defined PYTHON (
    where python >nul 2>nul
    if not errorlevel 1 python -c "import sys; raise SystemExit(0 if sys.version_info[0] == 3 else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON=python"
)

if not defined PYTHON (
    echo Python 3 is required. Install Python 3 from https://www.python.org/downloads/ and enable the PATH option, then run this file again.
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Lab03 virtual environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt || exit /b 1
if not exist "lab03.db" (
    ".venv\Scripts\python.exe" seed.py
    if errorlevel 1 exit /b 1
)
echo Lab03: http://127.0.0.1:5003 (Ctrl+C to stop)
".venv\Scripts\python.exe" app.py
exit /b %errorlevel%
