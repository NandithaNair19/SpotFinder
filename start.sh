#!/bin/bash

echo "Starting SpotFinder..."

source venv/bin/activate

echo "Starting telemetry server..."
cd telemetry-server
python3.11 server.py &
cd ..

sleep 3

echo "Starting edge device..."
cd edge-device
python3.11 device.py &
cd ..

sleep 3

echo "Launching dashboard..."

echo ""

echo "SpotFinder is running!"
echo ""
echo "Dashboard:"
echo "http://127.0.0.1:8000"
echo ""
echo "CounterFit:"
echo "http://127.0.0.1:5000"


cd web-dashboard
python3.11 app.py