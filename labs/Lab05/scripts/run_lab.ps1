$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $VenvPython)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3.12 -m venv (Join-Path $Root ".venv")
    } else {
        & python -m venv (Join-Path $Root ".venv")
    }
}

& $VenvPython -m pip install -r (Join-Path $Root "requirements.txt")
if (-not (Test-Path -LiteralPath (Join-Path $Root "lab05.sqlite3"))) {
    & $VenvPython (Join-Path $Root "seed.py")
}

Write-Host "Lab05: http://127.0.0.1:5005 (Ctrl+C de dung)"
& $VenvPython (Join-Path $Root "app.py")
