@echo off
cd /d "%~dp0"

echo ============================
echo    Game Archive - Starting
echo ============================
echo.

:: Install dependencies
echo [1/2] Installing dependencies...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo OK

:: Start app
echo [2/2] Starting...
python main.py

pause
