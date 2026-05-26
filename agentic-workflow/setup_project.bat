@echo off
echo ========================================
echo 🚀 Agentic Workflow Project Setup
echo ========================================
echo.
echo This will set up both:
echo 1. Thesis Editor (academic writing tool)
echo 2. Orchestration System (workflow automation)
echo.
echo ========================================

REM Check prerequisites
echo.
echo 🔍 Checking prerequisites...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed
    echo    Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check Docker (optional, for orchestration system)
docker --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Docker is not installed (optional for orchestration system)
    echo    Install from: https://www.docker.com/products/docker-desktop/
) else (
    echo ✅ Docker is installed
)

echo.
echo 📁 Setting up project structure...
echo.

REM Set up Thesis Editor
echo 📚 Setting up Thesis Editor...
cd thesis_editor
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo   Installing python-docx...
    pip install python-docx
    echo ✅ Thesis Editor setup complete
) else (
    echo ✅ Thesis Editor already set up
)
cd ..

echo.
REM Set up Orchestration System
echo 🔧 Setting up Orchestration System...
cd orchestration_system
if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo   Installing dependencies...
    pip install -r requirements.txt
    echo ✅ Orchestration System setup complete
) else (
    echo ✅ Orchestration System already set up
)
cd ..

echo.
echo ========================================
echo ✅ Project Setup Complete!
echo ========================================
echo.
echo 📋 Available Tools:
echo.
echo 1. Thesis Editor:
echo    cd thesis_editor
echo    run_thesis_editor.bat
echo.
echo 2. Orchestration System:
echo    cd orchestration_system
echo    start.bat
echo.
echo 📚 Documentation:
echo • thesis_editor\QUICK_START_GUIDE.md
echo • orchestration_system\SIMPLE_GUIDE.md
echo.
pause