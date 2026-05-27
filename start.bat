@echo off
cd /d "%~dp0"

echo ============================
echo    Game Archive - Starting
echo ============================
echo.

:: Install dependencies
echo [1/3] Installing dependencies...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo Failed to install dependencies. Run: pip install -r requirements.txt
    pause
    exit /b 1
)
echo OK

:: Start server
echo [2/3] Starting server...
start python main.py

:: Wait for server to start
timeout /t 2 /nobreak >nul

:: Open browser
echo [3/3] Opening browser...
start http://127.0.0.1:8000

echo.
echo Server started at http://127.0.0.1:8000
echo Close this window to stop the server.
echo.
pause
