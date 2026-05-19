#!/bin/bash

echo "Starting SpotFinder..."

echo "Installing dependencies..."
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install -r requirements-ml.txt

echo "Running smoke test..."
python3.11 smoke_test.py || exit 1

echo "Starting CounterFit..."
counterfit &
sleep 5

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
cd web-dashboard

echo ""

echo "SpotFinder is running!"
echo "Dashboard:"
echo "http://127.0.0.1:8000"
echo ""
echo "CounterFit:"
echo "http://127.0.0.1:5000"


python3.11 app.py