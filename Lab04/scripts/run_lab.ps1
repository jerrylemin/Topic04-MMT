$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
if (-not (Test-Path '.venv')) { py -3 -m venv .venv }
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
if (-not (Test-Path 'lab04.db')) { & '.\.venv\Scripts\python.exe' seed.py }
Write-Host 'Victim: http://127.0.0.1:5004'
Write-Host 'Attacker same-site: http://127.0.0.1:9004'
Write-Host 'Attacker cross-site: http://localhost:9004'
& '.\.venv\Scripts\python.exe' run_both.py
