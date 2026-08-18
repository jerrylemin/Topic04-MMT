$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw "WSL not found. Install Ubuntu/WSL or use Docker; native Windows GCC/GDB is not assumed."
}

$resolved = (Resolve-Path -LiteralPath $root).Path
if ($resolved -notmatch '^([A-Za-z]):\\(.*)$') { throw "Lab02 must be on a local Windows drive for this wrapper." }
$wslRoot = "/mnt/$($Matches[1].ToLower())/$($Matches[2] -replace '\\', '/')"
wsl.exe -d Ubuntu -- sh -lc "cd '$wslRoot' && sh scripts/build_all.sh"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
