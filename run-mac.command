#!/bin/bash

cd "$(dirname "$0")"

echo "Fixing permissions..."

chmod +x setup.sh
chmod +x start.sh

echo "Starting SpotFinder..."

if [ ! -d "venv" ]; then
    echo "First time setup..."
    bash setup.sh
fi

bash start.sh

echo ""
echo "Press any key to close..."
read -n 1