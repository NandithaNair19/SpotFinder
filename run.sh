#!/bin/bash


echo "Setting up SpotFinder..."


# Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
python3.11 -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-ml.txt

# Install CounterFit packages
pip install counterfit
pip install counterfit-connection
pip install counterfit-shims-serial
pip install counterfit-shims-picamera

# Run smoke test
echo "Running smoke test..."
python3.11 smoke_test.py || exit 1

# Start CounterFit
echo "Starting CounterFit..."
counterfit &
sleep 8

# Start telemetry server
echo "Starting telemetry server..."
cd telemetry-server
python3.11 server.py &
cd ..

sleep 3

# Start edge device
echo "Starting edge device..."
cd edge-device
python3.11 device.py &
cd ..

sleep 3

# Launch dashboard
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