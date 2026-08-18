@echo off
setlocal

where wsl.exe >nul 2>&1
if errorlevel 1 (
    echo [ERROR] WSL is not installed or wsl.exe is not available in PATH.
    echo Install WSL with an Ubuntu distro, then run this file again.
    exit /b 1
)

echo [INFO] Starting the Ubuntu WSL distro...
wsl.exe -d Ubuntu -- sh -lc "exit 0"
if errorlevel 1 (
    echo [ERROR] The Ubuntu WSL distro could not be started.
    echo Run "wsl.exe --list --verbose" to check the installed distro name.
    exit /b 1
)

call "%~dp0run_lab.bat"
exit /b %errorlevel%
