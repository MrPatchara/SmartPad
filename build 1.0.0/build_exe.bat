@echo off
REM Build script for Text Editor Plus using NUITKA
REM This script creates a standalone .exe file in current folder

echo ========================================
echo Building Text Editor Plus with NUITKA
echo ========================================
echo.

REM Change to project root directory
cd /d "%~dp0\.."

REM Check if NUITKA is installed
python -m nuitka --version >nul 2>&1
if errorlevel 1 (
    echo NUITKA is not installed. Installing...
    pip install nuitka
    if errorlevel 1 (
        echo Failed to install NUITKA. Please install manually: pip install nuitka
        pause
        exit /b 1
    )
)

echo.
echo Starting NUITKA build...
echo.

REM Build with NUITKA
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-icon-from-ico=src\icon.ico ^
    --output-dir="build 1.0.0" ^
    --output-filename=TextEditorPlus.exe ^
    --include-package-data=src ^
    --include-data-dir=src=src ^
    --include-data-files=src/logo.png=src/logo.png ^
    --include-data-files=src/icon.ico=src/icon.ico ^
    --enable-plugin=pyqt5 ^
    --windows-console-mode=disable ^
    --assume-yes-for-downloads ^
    --show-progress ^
    --show-memory ^
    --remove-output ^
    main.py

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo Output: build 1.0.0\TextEditorPlus.exe
echo ========================================
echo.
pause

