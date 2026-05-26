# PowerShell script to stop the orchestration system
# Equivalent to 'make stop'

Write-Host "🛑 Stopping Local Orchestration System..." -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan

# Stop services
docker-compose down

Write-Host "`n✅ Services stopped successfully!" -ForegroundColor Green
Write-Host "`n💡 To start services again, run: .\start.ps1" -ForegroundColor Cyan