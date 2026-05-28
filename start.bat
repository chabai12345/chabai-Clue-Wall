@echo off
cd /d "%~dp0"

echo ================================
echo    侦探看板 · Detective Board
echo ================================
echo.

:: Install dependencies
echo [1/3] Installing dependencies...
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)
echo OK

:: Start desktop app
echo [2/3] Starting desktop mode...
echo.
echo  Window: Frameless ^| Always-on-top
echo  Hotkey: Ctrl+Shift+D  (show/hide)
echo  Close:  Alt+F4
echo  Move:   Alt + drag
echo.

python desktop_app.py

pause
