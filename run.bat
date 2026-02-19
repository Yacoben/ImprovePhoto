@echo off
chcp 65001 >nul 2>&1
title ImprovePhoto - Poprawa jakości miniatur CAD

set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
if not exist "%PYTHON_PATH%" set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo ============================================
    echo   BŁĄD: Nie znaleziono instalacji Pythona!
    echo ============================================
    echo.
    echo Zainstaluj Python 3.12 lub 3.13
    echo.
    pause
    exit /b 1
)

"%PYTHON_PATH%" main.py %*

if errorlevel 1 (
    echo.
    echo ============================================
    echo   Program zakończył się z błędem
    echo ============================================
    echo.
    pause
)

