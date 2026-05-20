#!/bin/bash

cd "$(dirname "$0")"

echo "Removing macOS quarantine..."
xattr -dr com.apple.quarantine . 2>/dev/null

echo "Fixing permissions..."
chmod +x setup.sh
chmod +x start.sh

echo "Starting SpotFinder..."

if [ ! -d "venv" ]; then
    echo "First time setup..."
    /bin/bash setup.sh
fi

/bin/bash start.sh

echo ""
echo "Press any key to close..."
read -n 1