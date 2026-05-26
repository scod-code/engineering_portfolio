@echo off
echo 🔧 Setting up Python environment...
echo =====================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed
    echo    Please install Python from: https://www.python.org/downloads/
    echo    Make sure to check 'Add Python to PATH' during installation
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Create virtual environment
echo.
echo 📁 Creating virtual environment...
python -m venv venv

echo.
echo ✅ Virtual environment created!
echo.
echo 📋 Next steps:
echo    1. Activate the virtual environment:
echo       Command Prompt: venv\Scripts\activate.bat
echo       PowerShell: .\venv\Scripts\Activate.ps1
echo.
echo    2. Install dependencies:
echo       pip install -r requirements.txt
echo.
echo    3. Test the installation:
echo       python -c "import prefect; print('Prefect version:', prefect.__version__)"
echo.
echo 💡 Quick activation command:
echo    venv\Scripts\activate.bat
pause