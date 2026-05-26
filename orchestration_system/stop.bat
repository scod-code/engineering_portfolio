@echo off
echo 🛑 Stopping Local Orchestration System...
echo ==========================================

REM Stop services
docker-compose down

echo.
echo ✅ Services stopped successfully!
echo.
echo 💡 To start services again, run: start.bat
pause