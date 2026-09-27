@echo off
setlocal
cd /d "%~dp0"
python setup.py
if errorlevel 1 pause & exit /b 1
python main.py
if errorlevel 1 pause
