@echo off
REM WebDriver Cache Cleaner for POE2 Launcher
echo ================================
echo WebDriver Cache Cleaner
echo ================================
echo.

echo This will delete the WebDriver cache to fix common issues.
echo Cache location: %USERPROFILE%\.wdm
echo.

set /p confirm="Do you want to delete the cache? (y/n): "

if /i "%confirm%"=="y" (
    echo.
    echo Deleting WebDriver cache...
    rmdir /s /q "%USERPROFILE%\.wdm"

    if errorlevel 1 (
        echo.
        echo Failed to delete cache. It might not exist or is in use.
    ) else (
        echo.
        echo ================================
        echo Cache deleted successfully!
        echo ================================
        echo.
        echo The WebDriver will be downloaded again on next run.
    )
) else (
    echo.
    echo Cancelled.
)

echo.
pause
