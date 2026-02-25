@echo off
REM Social Media Dashboard - Quick Start
REM Starts the dashboard server and opens in browser

echo ========================================================================
echo   SOCIAL MEDIA DASHBOARD - STARTUP
echo ========================================================================
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo       Python found
echo.

echo [2/3] Installing dependencies...
pip install flask flask-cors requests python-dotenv twilio -q
echo       Dependencies installed
echo.

echo [3/3] Starting dashboard server...
echo.
echo ========================================================================
echo   DASHBOARD STARTING
echo ========================================================================
echo.
echo   Server URL: http://localhost:8081
echo   API URL:    http://localhost:8081/api
echo.
echo   Opening browser in 3 seconds...
echo.
echo   Press Ctrl+C to stop the server
echo ========================================================================
echo.

REM Start server in background
start "Dashboard Server" cmd /k "python dashboard_server.py"

REM Wait for server to start
timeout /t 3 /nobreak >nul

REM Open dashboard in default browser
start http://localhost:8081

echo.
echo   Dashboard opened in your browser!
echo   Keep this window open to maintain the server.
echo.
