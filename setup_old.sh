#!/bin/bash
 
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
 
echo ""

echo " SpotFinder Setup"

echo ""
 
read -p "Enter DB server: " DB_SERVER
read -p "Enter DB name [postgres]: " DB_NAME
DB_NAME=${DB_NAME:-postgres}
read -p "Enter DB user: " DB_USER
read -s -p "Enter DB password: " DB_PASSWORD
echo ""
read -p "Enter DB port [5432]: " DB_PORT
DB_PORT=${DB_PORT:-5432}
 
echo ""
echo "Creating .env files..."
 
cat > "$SCRIPT_DIR/telemetry-server/.env" <<EOF
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
 
cat > "$SCRIPT_DIR/web-dashboard/.env" <<EOF
SERVER=$DB_SERVER
DATABASE=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
PORT=$DB_PORT
EOF
 
cat > "$SCRIPT_DIR/edge-device/.env" <<EOF
DEVICE_NAME=edge-device
UUID=test-device
TOPIC=spotfinder_gps
DEBUG=0
EOF
 
echo ".env files created!"
 
echo ""
echo "Setting up virtual environment..."
 
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    python3.11 -m venv "$SCRIPT_DIR/venv"
fi
 
source "$SCRIPT_DIR/venv/bin/activate"
python3.11 -m pip install --upgrade pip
 
echo ""
echo "Installing dependencies..."
 
pip install -r "$SCRIPT_DIR/requirements.txt"
pip install -r "$SCRIPT_DIR/requirements-ml.txt"
pip install counterfit counterfit-connection counterfit-shims-serial counterfit-shims-picamera
 
echo ""

echo " Setup complete!"

echo ""
echo " Starting CounterFit on http://127.0.0.1:5000"
echo ""
echo " Please open http://127.0.0.1:5000 and configure:"
echo ""
echo "   1. Camera sensor:"
echo "      - Type: Camera"
echo "      - Port: PiCamera"
echo "      - Source: File"
echo "      - Image: parking.jpg"
echo ""
echo "   2. GPS sensor:"
echo "      - Type: UART GPS"
echo "      - Port: /dev/ttyAMA0"
echo "      - Source: Lat/Lon"
echo "      - Enable Repeat"
echo ""
echo " Once sensors are configured, come back here"
echo " and press Enter to launch SpotFinder."

echo ""
 
counterfit &
 
sleep 3
 
read -p "Press Enter when CounterFit sensors are configured..."
 
echo ""
echo "Launching SpotFinder..."
 
bash "$SCRIPT_DIR/start.sh"