@echo off
setlocal EnableExtensions EnableDelayedExpansion

where docker.exe >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker CLI is not installed or docker.exe is not available in PATH.
    echo Install Docker Desktop, then run this file again.
    exit /b 1
)

docker info >nul 2>&1
if not errorlevel 1 goto docker_ready

set "DOCKER_DESKTOP=%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
if not exist "!DOCKER_DESKTOP!" set "DOCKER_DESKTOP=%LocalAppData%\Docker\Docker Desktop.exe"

if not exist "!DOCKER_DESKTOP!" (
    echo [ERROR] Docker Engine is not running and Docker Desktop could not be found.
    echo Start Docker Desktop manually, then run this file again.
    exit /b 1
)

echo [INFO] Starting Docker Desktop...
start "" "!DOCKER_DESKTOP!"
echo [INFO] Waiting up to 180 seconds for Docker Engine...
call :wait_for_docker
if errorlevel 1 exit /b 1

:docker_ready
pushd "%~dp0.."
if errorlevel 1 (
    echo [ERROR] Could not open the Lab02 directory.
    exit /b 1
)

docker compose version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose v2 is not available.
    popd
    exit /b 1
)

echo [INFO] Starting Lab02 at http://127.0.0.1:5002
echo [INFO] Press Ctrl+C to stop the containers.
docker compose up --build
set "EXIT_CODE=!errorlevel!"
popd
exit /b !EXIT_CODE!

:wait_for_docker
set /a ATTEMPT=0
:wait_for_docker_loop
docker info >nul 2>&1
if not errorlevel 1 exit /b 0
set /a ATTEMPT+=1
if !ATTEMPT! geq 90 (
    echo [ERROR] Docker Engine did not become ready within 180 seconds.
    exit /b 1
)
timeout /t 2 /nobreak >nul
goto wait_for_docker_loop
