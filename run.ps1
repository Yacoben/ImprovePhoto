# Skrypt uruchamiający ImprovePhoto
# Automatycznie znajduje zainstalowaną wersję Pythona

$pythonPath = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"

if (-not (Test-Path $pythonPath)) {
    $pythonPath = "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
}

if (-not (Test-Path $pythonPath)) {
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "  Błąd: Nie znaleziono instalacji Pythona!" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Sprawdzone lokalizacje:" -ForegroundColor Yellow
    Write-Host "  - $env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
    Write-Host "  - $env:LOCALAPPDATA\Programs\Python\Python312\python.exe"
    Write-Host ""
    Write-Host "Zainstaluj Python 3.12 lub 3.13 i spróbuj ponownie." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host "============================================" -ForegroundColor Green
Write-Host "  ImprovePhoto - Poprawa jakości miniatur" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Python: " -NoNewline
Write-Host "$pythonPath" -ForegroundColor Cyan
Write-Host ""

# Uruchom program z przekazanymi argumentami
& $pythonPath "main.py" $args

# Sprawdź kod wyjścia
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Program zakończył się z błędem (kod: $LASTEXITCODE)" -ForegroundColor Red
    Write-Host ""
}

pause

