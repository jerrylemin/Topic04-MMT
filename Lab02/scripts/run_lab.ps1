$ErrorActionPreference = "Stop"
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = [Security.Principal.WindowsPrincipal]::new($identity)
if ($principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw "Do not run the lab from an Administrator PowerShell. Open a standard-user terminal."
}
if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
    throw "WSL not found. Use Docker or install Ubuntu/WSL for Linux GCC and GDB."
}
$root = Split-Path -Parent $PSScriptRoot
$resolved = (Resolve-Path -LiteralPath $root).Path
if ($resolved -notmatch '^([A-Za-z]):\\(.*)$') { throw "Lab02 must be on a local Windows drive for this wrapper." }
$wslRoot = "/mnt/$($Matches[1].ToLower())/$($Matches[2] -replace '\\', '/')"
wsl.exe -d Ubuntu -- sh -lc "cd '$wslRoot' && sh scripts/run_lab.sh"
exit $LASTEXITCODE
