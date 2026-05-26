# PowerShell script to run full demonstration
# Equivalent to running python demo_integration.py

Write-Host "🎯 Local Orchestration System Demonstration" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan

# Check prerequisites
Write-Host "`n📋 Checking prerequisites..." -ForegroundColor Cyan

# Check Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not running" -ForegroundColor Red
    Write-Host "   Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Check Docker Compose
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed" -ForegroundColor Red
    Write-Host "   Docker Compose should be included with Docker Desktop" -ForegroundColor Yellow
    exit 1
}

# Check Python
try {
    python --version | Out-Null
    Write-Host "✅ Python is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    Write-Host "   Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if services are running
Write-Host "`n🔍 Checking if services are running..." -ForegroundColor Cyan
try {
    $services = docker-compose ps 2>$null
    if ($services -match "Up") {
        Write-Host "✅ Services are running" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Services are not running. Starting them now..." -ForegroundColor Yellow
        .\start.ps1
        Start-Sleep -Seconds 15
    }
} catch {
    Write-Host "⚠️  Services are not running. Starting them now..." -ForegroundColor Yellow
    .\start.ps1
    Start-Sleep -Seconds 15
}

# Set up Python environment if needed
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "`n🔧 Setting up Python environment..." -ForegroundColor Yellow
    .\setup.ps1
    Write-Host "`n📋 Please activate the virtual environment and run the demo again:" -ForegroundColor Cyan
    Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "   .\demo.ps1" -ForegroundColor White
    exit 0
}

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "`n⚠️  Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "   Activating virtual environment..." -ForegroundColor Cyan
    
    # Try to activate
    try {
        & ".\venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } catch {
        Write-Host "❌ Could not activate virtual environment" -ForegroundColor Red
        Write-Host "   Please activate manually: .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "   Then run: .\demo.ps1" -ForegroundColor White
        exit 1
    }
}

# Install dependencies if needed
$requirementsCheck = python -c "import prefect" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Run the Python demo
Write-Host "`n🚀 Running demonstration..." -ForegroundColor Cyan
python demo_integration.py

Write-Host "`n✅ Demonstration completed!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Explore n8n at: http://localhost:5678" -ForegroundColor White
Write-Host "   2. Explore Prefect at: http://localhost:4200" -ForegroundColor White
Write-Host "   3. Run pipelines: .\run-pipeline.ps1" -ForegroundColor White
Write-Host "   4. Check status: .\status.ps1" -ForegroundColor White
Write-Host "   5. Stop services: .\stop.ps1" -ForegroundColor White