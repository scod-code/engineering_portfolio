# ASAA Fashion Beauty House - One-Click Startup
# Just run: .\start.ps1

Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Magenta
Write-Host "     ASAA Fashion & Beauty House            " -ForegroundColor Magenta
Write-Host "     Starting your website...               " -ForegroundColor Magenta
Write-Host "  ==========================================" -ForegroundColor Magenta
Write-Host ""

# --- Step 1: Check Python ---
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) { $pythonCmd = $cmd; break }
    } catch {}
}
if (-not $pythonCmd) {
    Write-Host "   Python not found. Please install Python 3.10+ from https://python.org" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "   $($pythonCmd) found" -ForegroundColor Green

# --- Step 2: Virtual environment ---
if (-not (Test-Path "backend\.venv")) {
    Write-Host "   Creating virtual environment (first time only)..." -ForegroundColor Yellow
    & $pythonCmd -m venv backend\.venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "   Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "   Virtual environment ready" -ForegroundColor Green
}

# --- Step 3: Activate & install ---
$activateScript = "backend\.venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "   Could not find activation script" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "   Installing dependencies..." -ForegroundColor Yellow
pip install -r backend\requirements.txt --quiet 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "   Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "   Dependencies installed" -ForegroundColor Green

# --- Step 4: Check .env ---
if (-not (Test-Path "backend\.env")) {
    Write-Host ""
    Write-Host "   No backend\.env file found." -ForegroundColor Yellow
    Write-Host "    Copying from .env.example  please edit it with your MongoDB credentials." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "   Created backend\.env (edit this file with your database details)" -ForegroundColor Green
}

# --- Step 5: Open browser & start server ---
Write-Host ""
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host "  Your website is starting at:" -ForegroundColor White
Write-Host ""
Write-Host "      http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "      http://127.0.0.1:8000/admin.html" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  Press Ctrl+C to stop the server." -ForegroundColor DarkGray
Write-Host "  ==========================================" -ForegroundColor Cyan
Write-Host ""

# Open the browser automatically after a short delay
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    Start-Process "http://127.0.0.1:8000"
} | Out-Null

# Start the server (this serves BOTH the API and the website)
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
