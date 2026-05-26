# PowerShell script to set up Python environment
# Equivalent to 'make setup'

Write-Host "🔧 Setting up Python environment..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan

# Check if Python is installed
try {
    python --version | Out-Null
    Write-Host "✅ Python is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    Write-Host "   Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment
Write-Host "`n📁 Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

Write-Host "`n✅ Virtual environment created!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Activate the virtual environment:" -ForegroundColor White
Write-Host "      PowerShell: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "      Command Prompt: venv\Scripts\activate.bat" -ForegroundColor White
Write-Host "`n   2. Install dependencies:" -ForegroundColor White
Write-Host "      pip install -r requirements.txt" -ForegroundColor White
Write-Host "`n   3. Test the installation:" -ForegroundColor White
Write-Host "      python -c \"import prefect; print('Prefect version:', prefect.__version__)\"" -ForegroundColor White
Write-Host "`n💡 Quick activation command:" -ForegroundColor Cyan
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White