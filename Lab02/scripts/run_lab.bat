@echo off
setlocal
cd /d "%~dp0.."
where wsl.exe >nul 2>nul || (
  echo WSL is required to build and run the Linux native binaries.
  exit /b 1
)
for /f "usebackq delims=" %%I in (`wsl.exe wslpath -a "%CD%"`) do set "WSL_ROOT=%%I"
if not defined WSL_ROOT exit /b 1
wsl.exe -d Ubuntu -- sh -lc "python3 -m pip --version >/dev/null 2>&1"
if errorlevel 1 goto windows_fallback
wsl.exe -d Ubuntu -- sh -lc "cd '%WSL_ROOT%' && python3 -m pip install --user --break-system-packages -r requirements.txt && make all && python3 app.py"
exit /b %errorlevel%

:windows_fallback
echo WSL Python has no pip; starting the web UI with Windows Python.
echo Native Linux demonstrations remain unavailable until python3-pip is installed in Ubuntu.
where py >nul 2>nul && (set "PYTHON=py -3.12") || (set "PYTHON=python")
%PYTHON% -m pip install --user -r requirements.txt || exit /b 1
%PYTHON% app.py
exit /b %errorlevel%
