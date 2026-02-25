#!/bin/bash
# Social Media Dashboard - Quick Start (Linux/Mac)

echo "========================================================================"
echo "  SOCIAL MEDIA DASHBOARD - STARTUP"
echo "========================================================================"
echo ""
echo "[1/3] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found! Please install Python 3.8+"
    exit 1
fi
echo "      Python found: $(python3 --version)"
echo ""

echo "[2/3] Installing dependencies..."
pip3 install flask flask-cors requests python-dotenv twilio -q
echo "      Dependencies installed"
echo ""

echo "[3/3] Starting dashboard server..."
echo ""
echo "========================================================================"
echo "  DASHBOARD STARTING"
echo "========================================================================"
echo ""
echo "  Server URL: http://localhost:8081"
echo "  API URL:    http://localhost:8081/api"
echo ""
echo "  Opening browser..."
echo ""
echo "  Press Ctrl+C to stop the server"
echo "========================================================================"
echo ""

# Start server
python3 dashboard_server.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Open dashboard in default browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8081
elif command -v open &> /dev/null; then
    open http://localhost:8081
else
    echo "  Please open http://localhost:8081 in your browser"
fi

echo ""
echo "  Dashboard server running (PID: $SERVER_PID)"
echo "  Keep this terminal open to maintain the server."
echo ""

# Wait for server process
wait $SERVER_PID
