@echo off
setlocal
cd /d "%~dp0"

if not exist ".jarvis_setup_done" (
    echo First launch - installing JARVIS...
    python setup.py
    if errorlevel 1 (
        echo.
        echo Setup failed.
        pause
        exit /b 1
    )
)

echo Starting JARVIS...
python main.py
if errorlevel 1 pause
