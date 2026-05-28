@echo off
cd /d "%~dp0"

echo ================================
echo    Building Detective Board
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

:: Clean previous build
echo [2/3] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo OK

:: PyInstaller
echo [3/3] Packaging EXE...
pyinstaller --onefile --windowed --name "侦探看板" ^
    --add-data "static;static" ^
    --collect-all "fastapi" ^
    --collect-all "uvicorn" ^
    --collect-all "starlette" ^
    --collect-all "pydantic" ^
    --hidden-import "uvicorn.loggers" ^
    --hidden-import "uvicorn.loops.auto" ^
    --hidden-import "uvicorn.protocols.http.auto" ^
    --hidden-import "uvicorn.protocols.websocket.auto" ^
    --hidden-import "uvicorn.middleware.asgi2" ^
    --hidden-import "uvicorn.middleware.wsgi" ^
    --exclude "PyQt5" --exclude "PySide6" --exclude "PySide2" --exclude "PyQt6" ^
    --exclude "matplotlib" --exclude "notebook" --exclude "ipython" --exclude "jupyter" ^
    --exclude "scipy" --exclude "pandas" ^
    desktop_app.py

if %errorlevel% neq 0 (
    echo Build failed.
    pause
    exit /b 1
)

echo.
echo ================================
echo    Build complete!
echo    dist\侦探看板.exe
echo ================================
pause
