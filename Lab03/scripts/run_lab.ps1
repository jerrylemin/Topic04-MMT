$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$Venv = Join-Path $Root '.venv'
if (-not (Test-Path $Venv)) { python -m venv $Venv }
$Python = Join-Path $Venv 'Scripts\python.exe'
& $Python -m pip install -r (Join-Path $Root 'requirements.txt')
if (-not (Test-Path (Join-Path $Root 'lab03.db'))) { & $Python (Join-Path $Root 'seed.py') }
Set-Location $Root
& $Python app.py
