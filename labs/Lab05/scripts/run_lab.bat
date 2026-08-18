@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_lab.ps1"
exit /b %errorlevel%
