# PowerShell script to start the orchestration system
# Equivalent to 'make start'

Write-Host "🚀 Starting Local Orchestration System..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan

# Check if Docker is running
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed or not running" -ForegroundColor Red
    Write-Host "   Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Check if Docker Compose is available
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed" -ForegroundColor Red
    Write-Host "   Docker Compose should be included with Docker Desktop" -ForegroundColor Yellow
    exit 1
}

# Start services
Write-Host "`n📦 Starting Docker services..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "`n⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host "`n🔍 Checking service status..." -ForegroundColor Cyan
docker-compose ps

Write-Host "`n✅ Services started successfully!" -ForegroundColor Green
Write-Host "`n🌐 Access Points:" -ForegroundColor Cyan
Write-Host "   • n8n:      http://localhost:5678" -ForegroundColor White
Write-Host "   • Prefect:  http://localhost:4200" -ForegroundColor White
Write-Host "`n🔑 Default credentials:" -ForegroundColor Cyan
Write-Host "   • n8n: admin / password123" -ForegroundColor White
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Open n8n in your browser: http://localhost:5678" -ForegroundColor White
Write-Host "   2. Open Prefect in your browser: http://localhost:4200" -ForegroundColor White
Write-Host "   3. Run '.\setup.ps1' to set up Python environment" -ForegroundColor White
Write-Host "   4. Run '.\run-pipeline.ps1' to test a pipeline" -ForegroundColor White