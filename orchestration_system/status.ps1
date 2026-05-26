# PowerShell script to check system status
# Equivalent to 'make status'

Write-Host "🔍 Local Orchestration System Status" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

# Check Docker services
Write-Host "`n📦 Docker Services:" -ForegroundColor Cyan
try {
    docker-compose ps
} catch {
    Write-Host "❌ Docker Compose not available or services not running" -ForegroundColor Red
}

# Check Python environment
Write-Host "`n🐍 Python Environment:" -ForegroundColor Cyan
try {
    python --version
} catch {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
}

# Check virtual environment
$venvPath = "venv"
if (Test-Path $venvPath) {
    Write-Host "✅ Virtual environment exists: $venvPath" -ForegroundColor Green
    
    # Check if activated
    if ($env:VIRTUAL_ENV) {
        Write-Host "✅ Virtual environment is activated" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Virtual environment not activated" -ForegroundColor Yellow
        Write-Host "   Activate with: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    }
} else {
    Write-Host "❌ Virtual environment not found" -ForegroundColor Red
    Write-Host "   Create with: .\setup.ps1" -ForegroundColor White
}

# Check output directories
Write-Host "`n📁 Output Directories:" -ForegroundColor Cyan
$directories = @("output", "data", "models", "reports", "ml_pipeline_output", "etl_output")
foreach ($dir in $directories) {
    if (Test-Path $dir) {
        $fileCount = (Get-ChildItem $dir -File | Measure-Object).Count
        Write-Host "   ✅ $dir/ ($fileCount files)" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $dir/ (not created)" -ForegroundColor Red
    }
}

# Check access URLs
Write-Host "`n🌐 Access URLs:" -ForegroundColor Cyan
Write-Host "   • n8n:      http://localhost:5678" -ForegroundColor White
Write-Host "   • Prefect:  http://localhost:4200" -ForegroundColor White

Write-Host "`n📋 Available Commands:" -ForegroundColor Cyan
Write-Host "   • .\start.ps1          - Start all services" -ForegroundColor White
Write-Host "   • .\stop.ps1           - Stop all services" -ForegroundColor White
Write-Host "   • .\setup.ps1          - Set up Python environment" -ForegroundColor White
Write-Host "   • .\run-pipeline.ps1   - Run example pipelines" -ForegroundColor White
Write-Host "   • .\demo.ps1           - Run full demonstration" -ForegroundColor White