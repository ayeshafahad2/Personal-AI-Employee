@echo off
REM Restart Dashboard Server with Fresh Credentials

echo Stopping existing Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting Dashboard Server...
echo.
echo ================================================================
echo   SOCIAL MEDIA DASHBOARD - FRESH START
echo ================================================================
echo.
echo   Dashboard URL: http://localhost:8081
echo.
echo   Platform Status:
echo   - Twitter:    READY (Green)
echo   - LinkedIn:   READY (Green)
echo   - Gmail:      Configured (Yellow)
echo   - WhatsApp:   Browser Ready (Yellow)
echo   - Facebook:   Not Configured (Red)
echo   - Instagram:  HIDDEN
echo.
echo ================================================================
echo.

REM Start server in new window
start "Dashboard Server" cmd /k "python dashboard_server.py"

echo Waiting for server to start...
timeout /t 5 /nobreak >nul

echo Opening dashboard in Chrome...
start chrome "http://localhost:8081"

echo.
echo Dashboard is now open!
echo.
echo Press any key to check server status...
pause >nul

powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8081/api/health'"

echo.
echo Done! Keep this window open to maintain the server.
