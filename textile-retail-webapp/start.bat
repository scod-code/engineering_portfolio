@echo off
setlocal

echo.
echo   ==========================================
echo      ASAA Fashion ^& Beauty House
echo      Starting your website...
echo   ==========================================
echo.

set "PYTHON_CMD="
if exist "backend\.venv\Scripts\python.exe" set "PYTHON_CMD=backend\.venv\Scripts\python.exe"

if not defined PYTHON_CMD (
  where python >nul 2>nul
  if %errorlevel%==0 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
  where py >nul 2>nul
  if %errorlevel%==0 set "PYTHON_CMD=py"
)

if not defined PYTHON_CMD (
  echo   Python not found. Please install Python 3.10+ from https://python.org
  echo.
  pause
  exit /b 1
)

echo   Using %PYTHON_CMD%

if not exist "backend\.venv" (
  echo   Creating virtual environment...
  %PYTHON_CMD% -m venv backend\.venv
  if errorlevel 1 (
    echo   Failed to create virtual environment.
    pause
    exit /b 1
  )
)

call backend\.venv\Scripts\activate.bat
if errorlevel 1 (
  echo   Could not activate virtual environment.
  pause
  exit /b 1
)

echo   Installing dependencies...
pip install -r backend\requirements.txt --quiet
if errorlevel 1 (
  echo   Failed to install dependencies.
  pause
  exit /b 1
)

if not exist "backend\.env" (
  echo   Creating backend\.env from template...
  copy "backend\.env.example" "backend\.env" >nul
  echo   Edit backend\.env with your MongoDB connection if registration/login should work.
)

if /i "%~1"=="--check" (
  echo   start.bat check passed.
  exit /b 0
)

set "PORT="
for /l %%P in (8000,1,8010) do (
  netstat -ano | findstr /r /c:":%%P .*LISTENING" >nul
  if errorlevel 1 (
    set "PORT=%%P"
    goto :port_found
  )
)

echo   No free port found between 8000 and 8010.
pause
exit /b 1

:port_found

echo.
echo   Website:
echo      http://127.0.0.1:%PORT%
echo.
echo   Admin:
echo      http://127.0.0.1:%PORT%/admin.html
echo.
echo   Press Ctrl+C to stop the server.
echo.

start "" "http://127.0.0.1:%PORT%"
uvicorn backend.main:app --reload --host 127.0.0.1 --port %PORT%
