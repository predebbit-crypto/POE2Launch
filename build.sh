#!/bin/bash
# POE2 Launcher Build Script for Linux/Mac

echo "================================"
echo "POE2 Auto Login Launcher Builder"
echo "================================"
echo ""

echo "[1/3] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/3] Building executable..."
pyinstaller --onefile --name "POE2_Launcher" poe2_launcher.py
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build executable"
    exit 1
fi

echo ""
echo "[3/3] Copying config example..."
mkdir -p dist
cp config.json.example dist/config.json.example
if [ ! -f "dist/config.json" ]; then
    cp config.json.example dist/config.json
    echo "Created default config.json"
fi

echo ""
echo "================================"
echo "Build Complete!"
echo "================================"
echo ""
echo "Executable location: dist/POE2_Launcher"
echo ""
echo "Next steps:"
echo "1. Go to 'dist' folder"
echo "2. Edit config.json with your Daum account credentials"
echo "3. Run ./POE2_Launcher"
echo ""
