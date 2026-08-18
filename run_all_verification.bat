@echo off
setlocal EnableExtensions
cd /d "%~dp0"

where docker >nul 2>nul || (echo ERROR: docker CLI was not found.& pause & exit /b 1)
docker info >nul 2>nul || (echo ERROR: Docker daemon is not running.& pause & exit /b 1)

for %%L in (Lab01 Lab02 Lab03 Lab04 Lab05 Lab06) do (
  echo [START] %%L
  pushd "%%L"
  docker compose up -d --build || (popd & echo ERROR: %%L failed to start.& pause & exit /b 1)
  popd
)

echo [WAIT] Waiting for localhost health endpoints...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ports=5000,5002,5003,5004,5005,5006,9004; foreach($p in $ports){$ok=$false; 1..60|%%{try{$r=Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri ('http://127.0.0.1:'+$p+'/health'); if($r.StatusCode -eq 200){$ok=$true;break}}catch{};Start-Sleep -Seconds 1};if(-not $ok){throw ('Port '+$p+' did not become healthy')}}"
if errorlevel 1 (echo ERROR: One or more labs did not become healthy.& pause & exit /b 1)

set "VERIFY_PY=Lab03\.venv\Scripts\python.exe"
if not exist "%VERIFY_PY%" set "VERIFY_PY=python"
"%VERIFY_PY%" -m pytest -q verification --tb=short || (echo ERROR: HTTP verification failed.& pause & exit /b 1)
powershell -NoProfile -ExecutionPolicy Bypass -File verification\playwright_lab_flows.ps1 || (echo ERROR: Browser verification failed.& pause & exit /b 1)

echo PASS: all Topic04 HTTP and browser verification checks completed.
exit /b 0
