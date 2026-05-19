#!/bin/bash

echo "Starting SpotFinder setup..."

echo "Installing core dependencies..."
python3.11 -m pip install -r requirements.txt

echo "Installing ML dependencies..."
python3.11 -m pip install -r requirements-ml.txt

echo "Running smoke test..."
python3.11 smoke_test.py

echo "Launching dashboard..."
cd web-dashboard

echo "Dashboard running at:"
echo "http://127.0.0.1:8000"

python3.11 app.py