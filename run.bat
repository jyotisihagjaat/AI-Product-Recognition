@echo off
title AI Product Recognition
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Setup has not been completed yet.
    echo Run setup.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" src\recognize.py
if errorlevel 1 (
    echo.
    echo The app stopped. See the message above.
    pause
)
