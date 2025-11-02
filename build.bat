@echo off
REM POE2 Launcher Build Script for Windows
echo ================================
echo POE2 Auto Login Launcher Builder
echo ================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Building executable...
pyinstaller --onefile --noconsole --name "POE2_Launcher" --icon=NONE poe2_launcher.py
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)

echo.
echo [3/3] Copying config example...
if not exist "dist" mkdir dist
copy config.json.example dist\config.json.example
if not exist "dist\config.json" (
    copy config.json.example dist\config.json
    echo Created default config.json
)

echo.
echo ================================
echo Build Complete!
echo ================================
echo.
echo Executable location: dist\POE2_Launcher.exe
echo.
echo Next steps:
echo 1. Go to 'dist' folder
echo 2. Edit config.json with your Daum account credentials
echo 3. Run POE2_Launcher.exe
echo.
pause
