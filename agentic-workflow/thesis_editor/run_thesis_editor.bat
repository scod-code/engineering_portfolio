@echo off
echo ========================================
echo 📚 MSc Thesis Editor - Ready to Use
echo ========================================
echo.
echo This editor will help you fix:
echo • Week ranges (Weeks 1-8 → Weeks 1–8)
echo • Em-dashes (— → : or ,)
echo • Stock phrases and clarity issues
echo.
echo ========================================

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated
) else (
    echo ❌ Virtual environment not found
    echo    Creating one now...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install python-docx
)

REM Check for .docx files
echo.
echo 📁 Looking for .docx files...
dir *.docx /b

echo.
echo 🚀 Starting thesis editor...
echo.
echo If it asks for file path, enter: C:\Users\somto\Documents\Agentic Workflow\YOUR_FILE.docx
echo.
echo 💡 Place your thesis .docx file in this folder first!
echo.

REM Run the editor
python thesis_editor.py

echo.
echo ========================================
echo ✅ Editor completed
echo ========================================
echo.
echo Your files:
echo • thesis_backup_*.docx - Original backup
echo • thesis_edited_*.docx - Edited version
echo • thesis_changes.json - List of all changes
echo.
pause
