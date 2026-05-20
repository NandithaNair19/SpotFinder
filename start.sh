#!/bin/bash
 

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
 
echo "Starting SpotFinder..."
 
source "$SCRIPT_DIR/venv/bin/activate"
 
echo "Starting telemetry server..."
cd "$SCRIPT_DIR/telemetry-server"
python3.11 server.py &
SERVER_PID=$!
cd "$SCRIPT_DIR"
 
sleep 3
 
echo "Starting edge device..."
cd "$SCRIPT_DIR/edge-device"
python3.11 device.py &
DEVICE_PID=$!
cd "$SCRIPT_DIR"
 
sleep 3
 
echo "Starting dashboard..."
cd "$SCRIPT_DIR/web-dashboard"
python3.11 app.py &
DASHBOARD_PID=$!
cd "$SCRIPT_DIR"
 
sleep 2
 
echo ""

echo " SpotFinder is running!"

echo ""
echo " Dashboard:   http://127.0.0.1:8000"
echo " CounterFit:  http://127.0.0.1:5000"
echo ""
echo " Press Ctrl+C to stop all services."

 
# Keep script alive and kill all child processes on exit
trap "echo 'Stopping SpotFinder...'; kill $SERVER_PID $DEVICE_PID $DASHBOARD_PID 2>/dev/null; exit" SIGINT SIGTERM
 
wait