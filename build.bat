@echo off
cd /d "%~dp0"

echo ================================
echo   Game Archive - Build EXE
echo ================================
echo.

:: Install PyInstaller if needed
echo [1/3] Checking PyInstaller...
pip install pyinstaller -q

:: Build
echo [2/3] Building EXE...
pyinstaller --onefile --windowed --name "GameArchive" --add-data "data;data" main.py

echo [3/3] Done!
echo.
echo EXE created: dist\GameArchive.exe
echo.
pause
