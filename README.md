# ImprovePhoto - Program do poprawiania jakości miniatur CAD

Program do poprawiania jakości zdjęć miniatur elementów konstrukcyjnych z programu CAD Inventor.
Pogrubia czarne linie na białym tle dla lepszej widoczności w dokumentach PDF.

## Wymagania

- Python 3.12 lub nowszy
- Zainstalowane pakiety: opencv-python, numpy, Pillow (automatycznie zainstalowane z requirements.txt)

## Instalacja

Pakiety zostały już zainstalowane. W razie potrzeby reinstalacji:

```batch
C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```

## Użycie

### Metoda 1: Użycie skryptu run.bat (ZALECANE)

Najprościej uruchomić program korzystając z przygotowanego skryptu `run.bat`:

```batch
run.bat -d "ścieżka\do\katalogu" -r
```

### Metoda 2: Bezpośrednie uruchomienie Pythona

```batch
C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe main.py [opcje]
```

## Opcje programu

- `input` - Ścieżka do pojedynczego pliku PNG do przetworzenia
- `-o`, `--output` - Ścieżka do pliku wyjściowego
- `-d`, `--directory` - Katalog z plikami do przetworzenia
- `-od`, `--output-dir` - Katalog na pliki wyjściowe (jeśli nie podano, nadpisuje oryginały)
- `-t`, `--thickness` - Grubość pogrubienia linii (1-5, domyślnie: 4)
- `-c`, `--contrast` - Współczynnik kontrastu (domyślnie: 2.5)
- `-ns`, `--no-sharpen` - Wyłącz wyostrzanie
- `-r`, `--recursive` - Przetwarzaj podkatalogi rekurencyjnie
- `-e`, `--extra-enhance` - Dodatkowe wzmocnienie dla MAKSYMALNEJ widoczności linii

## Przykłady użycia

### Przetwarzanie pojedynczego pliku (nadpisanie oryginału):
```batch
run.bat obraz.png
```

### Przetwarzanie pojedynczego pliku (z zachowaniem oryginału):
```batch
run.bat obraz.png -o obraz_poprawiony.png
```

### Przetwarzanie całego katalogu (nadpisywanie plików w miejscu):
```batch
run.bat -d "X:\0.0.0.0 MINIATURY ELEMENTÓW" -r
```

### Przetwarzanie z maksymalną widocznością linii:
```batch
run.bat -d "X:\0.0.0.0 MINIATURY ELEMENTÓW" -r -e
```

### Przetwarzanie z niestandardowymi parametrami:
```batch
run.bat -d ".\zdjecia" -r -t 5 -c 3.0 -e
```
(Maksymalna grubość linii: 5, wysoki kontrast: 3.0, dodatkowe wzmocnienie)

### Przetwarzanie do osobnego katalogu (zachowuje oryginały):
```batch
run.bat -d ".\zdjecia" -od ".\zdjecia_poprawione" -r
```

## Jak działa program

Program wykonuje następujące operacje:

1. **Wczytanie obrazu** - Obsługuje PNG z przezroczystością i polskimi znakami w ścieżce
2. **Konwersja do skali szarości** - Przygotowanie do analizy
3. **Zwiększenie kontrastu** - Wstępne zwiększenie różnicy między liniami a tłem
4. **Binaryzacja adaptacyjna** - Wykrywa linie o różnej intensywności (2 metody łączone)
5. **Pogrubienie linii** - Dylacja morfologiczna z konfigurowalnymi parametrami
6. **Dodatkowe wzmocnienie** (opcja `-e`):
   - Dodatkowa dylacja dla wygładzenia linii
   - Morfologiczne zamknięcie - łączy przerwane linie
7. **Zwiększenie kontrastu CLAHE** - Adaptacyjna normalizacja
8. **Wyostrzanie** - Kernel sharpening dla lepszej ostrości krawędzi
9. **Zapis z kompresją** - PNG z maksymalną kompresją dla mniejszych plików

## Rozwiązywanie problemów

### Błąd: "Nie można wczytać obrazu"
- Sprawdź czy ścieżka jest poprawna
- Upewnij się, że plik jest w formacie PNG
- Sprawdź czy masz uprawnienia do odczytu pliku

### Linie są za cienkie
Użyj opcji `-e` (extra-enhance) dla maksymalnej widoczności:
```batch
run.bat -d "katalog" -r -e
```

Lub zwiększ parametr thickness do 5:
```batch
run.bat -d "katalog" -r -t 5
```

### Linie są za grube
Zmniejsz parametr thickness:
```batch
run.bat -d "katalog" -r -t 2
```

### Program nie znajduje Pythona
Upewnij się, że Python 3.13 jest zainstalowany w:
`C:\Users\User\AppData\Local\Programs\Python\Python313\`

## Uwagi

- Program domyślnie **nadpisuje oryginalne pliki** - upewnij się, że masz kopię zapasową lub użyj opcji `-od` do zapisu w osobnym katalogu
- Opcja `-r` (recursive) przeszukuje wszystkie podkatalogi
- Program przetwarza tylko pliki PNG
- Zachowuje kanał alfa (przezroczystość) jeśli istnieje

## Autor

Program stworzony do poprawy jakości miniatur elementów konstrukcyjnych z CAD Inventor dla celów dokumentacji PDF.

