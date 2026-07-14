$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $Root
$Python = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    py -3.12 -m venv .venv
}

& $Python -m pip install -r requirements.txt
$Database = Join-Path $Root "data\lab06.sqlite3"
if (-not (Test-Path -LiteralPath $Database)) {
    & $Python scripts\reset_database.py
}
Write-Host "Lab06: http://127.0.0.1:5006 (Ctrl+C to stop)"
& $Python app.py
