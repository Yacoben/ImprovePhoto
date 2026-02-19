@echo off
chcp 65001 >nul
echo ========================================
echo   IMPROVE PHOTO - Quick Process
echo ========================================
echo.

set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
if not exist "%PYTHON_PATH%" set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python312\python.exe

if not exist "%PYTHON_PATH%" (
    echo Błąd: Nie znaleziono instalacji Pythona!
    pause
    exit /b 1
)

echo Podaj ścieżkę do katalogu z miniaturami:
set /p KATALOG="Ścieżka: "

if "%KATALOG%"=="" (
    echo Nie podano ścieżki!
    pause
    exit /b 1
)

echo.
echo Wybierz tryb przetwarzania:
echo.
echo 1. Standardowy (grubość 4, kontrast 2.5)
echo 2. Maksymalne wzmocnienie (grubość 4, kontrast 2.5 + extra enhance)
echo 3. Ultra grube linie (grubość 5, kontrast 3.0 + extra enhance)
echo 4. Delikatne (grubość 2, kontrast 1.5)
echo.
set /p TRYB="Wybór (1-4): "

if "%TRYB%"=="1" (
    echo.
    echo Przetwarzanie w trybie standardowym...
    "%PYTHON_PATH%" main.py -d "%KATALOG%" -r
) else if "%TRYB%"=="2" (
    echo.
    echo Przetwarzanie z maksymalnym wzmocnieniem...
    "%PYTHON_PATH%" main.py -d "%KATALOG%" -r -e
) else if "%TRYB%"=="3" (
    echo.
    echo Przetwarzanie ULTRA - maksymalne grubienie...
    "%PYTHON_PATH%" main.py -d "%KATALOG%" -r -t 5 -c 3.0 -e
) else if "%TRYB%"=="4" (
    echo.
    echo Przetwarzanie delikatne...
    "%PYTHON_PATH%" main.py -d "%KATALOG%" -r -t 2 -c 1.5
) else (
    echo Nieprawidłowy wybór!
    pause
    exit /b 1
)

echo.
echo ========================================
pause

