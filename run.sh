#!/bin/bash

echo "Starting SpotFinder setup..."

python3.11 -m pip install -r requirements.txt
python3.11 -m pip install -r requirements-ml.txt

echo "Running smoke test..."
python3.11 smoke_test.py || exit 1

echo "Starting telemetry server..."
cd telemetry-server
python3.11 server.py &
cd ..

echo "Launching dashboard..."
cd web-dashboard

echo "Dashboard running at:"
echo "http://127.0.0.1:8000"

python3.11 app.py