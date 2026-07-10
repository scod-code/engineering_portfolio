@echo off
echo ========================================
echo 📚 MSc Thesis Document Editor
echo ========================================
echo.
echo This tool helps you edit your COMP40321 Research Methods
echo submission for your MSc in Robotics and Intelligent Systems.
echo.
echo Features:
echo • Fix punctuation (em-dashes, semicolons)
echo • Review stock phrases and clarity
echo • Compare wording with an optional rewriting service
echo • Work section-by-section with approval
echo.
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv\Scripts\python.exe" (
    echo ✅ Using virtual environment
    set PYTHON_EXE=venv\Scripts\python.exe
) else (
    echo ⚠️  Using system Python (virtual environment not found)
    set PYTHON_EXE=python
)

REM Run the editor
echo.
echo 🚀 Starting Academic Document Editor...
echo.
%PYTHON_EXE% academic_editor.py

echo.
echo ========================================
echo ✅ Editor completed
echo ========================================
echo.
echo Your edited files:
echo • *.backup_* - Original backup
echo • *.edited_* - Edited version
echo • *.changes.json - List of all changes made
echo.
echo 💡 Tips:
echo 1. Always review changes before final submission
echo 2. Keep backups of all versions
echo 3. Use section-by-section editing for control
echo.
pause
