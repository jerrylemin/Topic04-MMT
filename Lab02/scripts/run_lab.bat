@echo off
setlocal
cd /d "%~dp0.."
where wsl.exe >nul 2>nul
if errorlevel 1 goto windows_fallback
for /f "usebackq delims=" %%I in (`wsl.exe -d Ubuntu -- wslpath -a "%CD:\=/%"`) do set "WSL_ROOT=%%I"
if not defined WSL_ROOT goto windows_fallback
wsl.exe -d Ubuntu -- sh -lc "python3 -m pip --version >/dev/null 2>&1"
if errorlevel 1 goto windows_fallback
wsl.exe -d Ubuntu -- sh -lc "cd '%WSL_ROOT%' && if [ ! -x .venv/bin/python ]; then python3 -m venv .venv || exit 1; fi"
if errorlevel 1 goto windows_fallback
wsl.exe -d Ubuntu -- sh -lc "cd '%WSL_ROOT%' && .venv/bin/python -m pip install -r requirements.txt && make all && .venv/bin/python app.py"
exit /b %errorlevel%

:windows_fallback
echo WSL/Ubuntu with Python 3 and pip is unavailable; starting the web UI with Windows Python.
echo Native Linux demonstrations remain unavailable until WSL, Ubuntu, GCC, Make and GDB are installed.

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
    echo Python 3 is required for the Windows fallback. Install Python 3 and run this file again.
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating Lab02 Windows virtual environment...
    %PYTHON% -m venv .venv
    if errorlevel 1 exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt || exit /b 1
echo Lab02 web UI: http://127.0.0.1:5002 (Ctrl+C to stop)
".venv\Scripts\python.exe" app.py
exit /b %errorlevel%
