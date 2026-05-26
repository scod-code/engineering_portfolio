@echo off
echo 🚀 Starting Local Orchestration System...
echo ==========================================

REM Check if Docker is running
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not running
    echo    Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo ✅ Docker is installed

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed
    echo    Docker Compose should be included with Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker Compose is installed

REM Start services
echo.
echo 📦 Starting Docker services...
docker-compose up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check service status
echo.
echo 🔍 Checking service status...
docker-compose ps

echo.
echo ✅ Services started successfully!
echo.
echo 🌐 Access Points:
echo    • n8n:      http://localhost:5678
echo    • Prefect:  http://localhost:4200
echo.
echo 🔑 Default credentials:
echo    • n8n: admin / password123
echo.
echo 📋 Next steps:
echo    1. Open n8n in your browser: http://localhost:5678
echo    2. Open Prefect in your browser: http://localhost:4200
echo    3. Run 'setup.bat' to set up Python environment
echo    4. Run 'run-pipeline.bat' to test a pipeline
pause