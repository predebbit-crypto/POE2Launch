@echo off
REM POE2 Launcher Build Script for Windows
echo ================================
echo POE2 Auto Login Launcher Builder
echo ================================
echo.

REM Check if Python is installed
echo [0/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Python is not installed!
    echo ========================================
    echo.
    echo Python is required to build this project.
    echo.
    echo Please follow these steps:
    echo 1. Download Python from: https://www.python.org/downloads/
    echo 2. Run the installer
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation!
    echo 4. Restart your command prompt
    echo 5. Run build.bat again
    echo.
    echo ========================================
    pause
    exit /b 1
)

python --version
echo Python found!
echo.

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Building launcher executable...
pyinstaller --onefile --noconsole --name "POE2_Launcher" --icon=NONE poe2_launcher.py
if errorlevel 1 (
    echo ERROR: Failed to build launcher
    pause
    exit /b 1
)

echo.
echo [3/4] Building config setup tool...
pyinstaller --onefile --name "POE2_Setup" --icon=NONE setup_config.py
if errorlevel 1 (
    echo ERROR: Failed to build setup tool
    pause
    exit /b 1
)

echo.
echo [4/4] Copying config example...
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
echo Files created:
echo - POE2_Launcher.exe : Main launcher
echo - POE2_Setup.exe    : Account setup tool
echo.
echo Next steps:
echo 1. Go to 'dist' folder
echo 2. Run POE2_Setup.exe to configure your account
echo    OR manually edit config.json
echo 3. Run POE2_Launcher.exe to start the game
echo.
pause
