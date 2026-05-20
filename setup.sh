#!/bin/bash

echo "Setting up SpotFinder..."

echo ""
read -p "Enter DB server: " DB_SERVER
read -p "Enter DB name [postgres]: " DB_NAME
DB_NAME=${DB_NAME:-postgres}

read -p "Enter DB user: " DB_USER
read -s -p "Enter DB password: " DB_PASSWORD
echo ""

read -p "Enter DB port [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}

echo "Creating .env files..."

cat > telemetry-server/.env <<EOF
DRIVERNAME=postgresql+psycopg2
SERVER=$DB_SERVER
DATABASE=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
PORT=$DB_PORT
UUID=test-device
DEVICE_NAME=telemetry-server
TOPIC=spotfinder_gps
EOF

cat > web-dashboard/.env <<EOF
SERVER=$DB_SERVER
DATABASE=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
PORT=$DB_PORT
EOF

cat > edge-device/.env <<EOF
DEVICE_NAME=edge-device
UUID=test-device
TOPIC=spotfinder_gps
DEBUG=0
EOF

if [ ! -d "venv" ]; then
    python3.11 -m venv venv
fi

source venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt
pip install -r requirements-ml.txt

pip install counterfit
pip install counterfit-connection
pip install counterfit-shims-serial
pip install counterfit-shims-picamera

echo ""

echo "Setup complete!"
echo ""
echo "CounterFit is starting now."
echo ""
echo "Open:"
echo "http://127.0.0.1:5000"
echo ""
echo "Configure CounterFit:"
echo "- PiCamera"
echo "- GPS UART on /dev/ttyAMA0"
echo ""
echo "After CounterFit setup, open a new terminal and run:"
echo "./start.sh"

counterfit