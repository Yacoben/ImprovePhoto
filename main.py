"""
Program do poprawiania jakości zdjęć miniatur elementów konstrukcyjnych.
Pogrubia czarne linie na białym tle dla lepszej widoczności w dokumentach PDF.
"""

import sys
from pathlib import Path
import numpy as np
import cv2


def enhance_cad_image(input_path: str, output_path: str, line_thickness: int = 4,
                       contrast_boost: float = 2.5, sharpen: bool = True,
                       extra_enhance: bool = False) -> bool:
    """
    Poprawia jakość zdjęcia CAD poprzez pogrubienie linii i zwiększenie kontrastu.

    Args:
        input_path: Ścieżka do pliku wejściowego
        output_path: Ścieżka do pliku wyjściowego
        line_thickness: Grubość pogrubienia linii (1-5, domyślnie 4)
        contrast_boost: Współczynnik zwiększenia kontrastu (domyślnie 2.5)
        sharpen: Czy zastosować wyostrzanie (domyślnie True)
        extra_enhance: Czy zastosować dodatkowe wzmocnienie dla maksymalnej widoczności (domyślnie False)

    Returns:
        True jeśli operacja się powiodła, False w przeciwnym razie
    """
    try:
        # Wczytaj obraz - używamy numpy do obsługi ścieżek z polskimi znakami
        # cv2.imread nie obsługuje poprawnie Unicode w ścieżkach na Windows
        img = cv2.imdecode(np.fromfile(input_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

        if img is None:
            print(f"Błąd: Nie można wczytać obrazu: {input_path}")
            return False

        # Sprawdź czy obraz ma kanał alfa (przezroczystość)
        has_alpha = img.shape[2] == 4 if len(img.shape) == 3 else False

        if has_alpha:
            # Rozdziel kanały
            bgr = img[:, :, :3]
            alpha = img[:, :, 3]
        else:
            bgr = img
            alpha = None

        # Konwersja do skali szarości
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        # Najpierw zwiększ kontrast w skali szarości dla lepszego wykrycia linii
        gray = cv2.convertScaleAbs(gray, alpha=1.3, beta=-20)

        # Binaryzacja adaptacyjna - lepiej wykrywa linie o różnej intensywności
        # Kombinacja dwóch metod dla najlepszego rezultatu
        binary1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
        _, binary2 = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

        # Połącz obie metody (OR) - wykryje więcej linii
        binary = cv2.bitwise_or(binary1, binary2)

        # Pogrubienie linii za pomocą dylacji - używamy więcej iteracji dla silniejszego efektu
        if line_thickness > 0:
            kernel_size = max(2, line_thickness)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
            # Zwiększamy liczbę iteracji dla grubszych linii
            iterations = 1 if line_thickness <= 2 else 2
            binary = cv2.dilate(binary, kernel, iterations=iterations)

        # Dodatkowe wzmocnienie dla maksymalnej widoczności
        if extra_enhance:
            # Dodatkowa dylacja z mniejszym jądrem dla wygładzenia
            kernel_smooth = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            binary = cv2.dilate(binary, kernel_smooth, iterations=1)
            # Morfologiczne zamknięcie - łączy przerwane linie
            kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_close)

        # Inwersja z powrotem: białe linie na czarnym tle -> czarne linie na białym tle
        result_gray = cv2.bitwise_not(binary)

        # Konwersja z powrotem do BGR
        result = cv2.cvtColor(result_gray, cv2.COLOR_GRAY2BGR)

        # Zwiększenie kontrastu
        if contrast_boost != 1.0:
            # Normalizacja kontrastu
            lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=contrast_boost, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab = cv2.merge([l, a, b])
            result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # Wyostrzanie
        if sharpen:
            kernel_sharpen = np.array([[-1, -1, -1],
                                       [-1,  9, -1],
                                       [-1, -1, -1]])
            result = cv2.filter2D(result, -1, kernel_sharpen)

        # Przywróć kanał alfa jeśli istniał
        if has_alpha:
            result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
            result[:, :, 3] = alpha

        # Zapisz wynik - używamy imencode + tofile dla obsługi polskich znaków w ścieżce
        # Określ rozszerzenie pliku dla kodowania
        ext = Path(output_path).suffix.lower()
        if ext == '.png':
            encode_param = [cv2.IMWRITE_PNG_COMPRESSION, 9]
        elif ext in ['.jpg', '.jpeg']:
            encode_param = [cv2.IMWRITE_JPEG_QUALITY, 95]
        else:
            encode_param = []

        success, encoded_img = cv2.imencode(ext, result, encode_param)
        if success:
            encoded_img.tofile(output_path)
            print(f"Zapisano: {output_path}")
            return True
        else:
            print(f"Błąd: Nie można zakodować obrazu: {output_path}")
            return False

    except Exception as e:
        print(f"Błąd podczas przetwarzania {input_path}: {str(e)}")
        return False


def process_directory(input_dir: str, output_dir: str = None,
                      line_thickness: int = 4, contrast_boost: float = 2.5,
                      sharpen: bool = True, recursive: bool = True,
                      extra_enhance: bool = False) -> tuple:
    """
    Przetwarza wszystkie obrazy PNG w katalogu.

    Args:
        input_dir: Katalog z plikami wejściowymi
        output_dir: Katalog na pliki wyjściowe (domyślnie: nadpisuje oryginalne pliki)
        line_thickness: Grubość pogrubienia linii (domyślnie 4)
        contrast_boost: Współczynnik zwiększenia kontrastu (domyślnie 2.5)
        sharpen: Czy zastosować wyostrzanie (domyślnie True)
        recursive: Czy przetwarzać podkatalogi (domyślnie True)
        extra_enhance: Czy zastosować dodatkowe wzmocnienie (domyślnie False)

    Returns:
        Tuple (liczba_przetworzonych, liczba_błędów)
    """
    input_path = Path(input_dir)

    if not input_path.exists():
        print(f"Błąd: Katalog nie istnieje: {input_dir}")
        return (0, 0)

    # Jeśli nie podano output_dir, pliki będą nadpisywane w miejscu
    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = None  # Nadpisywanie w miejscu

    # Znajdź pliki PNG
    if recursive:
        png_files = list(input_path.rglob("*.png"))
    else:
        png_files = list(input_path.glob("*.png"))

    if not png_files:
        print(f"Nie znaleziono plików PNG w: {input_dir}")
        return (0, 0)

    print(f"Znaleziono {len(png_files)} plików PNG do przetworzenia.")

    success_count = 0
    error_count = 0

    for png_file in png_files:
        if output_path is not None:
            # Zachowaj strukturę katalogów jeśli recursive
            if recursive:
                relative = png_file.relative_to(input_path)
                output_file = output_path / relative
                output_file.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_file = output_path / png_file.name
        else:
            # Nadpisuj oryginalny plik
            output_file = png_file

        if enhance_cad_image(str(png_file), str(output_file),
                             line_thickness, contrast_boost, sharpen, extra_enhance):
            success_count += 1
        else:
            error_count += 1

    return (success_count, error_count)


def process_single_file(input_file: str, output_file: str = None,
                        line_thickness: int = 4, contrast_boost: float = 2.5,
                        sharpen: bool = True, extra_enhance: bool = False) -> bool:
    """
    Przetwarza pojedynczy plik obrazu.

    Args:
        input_file: Ścieżka do pliku wejściowego
        output_file: Ścieżka do pliku wyjściowego (domyślnie: nadpisuje oryginalny plik)
        line_thickness: Grubość pogrubienia linii
        contrast_boost: Współczynnik zwiększenia kontrastu
        sharpen: Czy zastosować wyostrzanie
        extra_enhance: Czy zastosować dodatkowe wzmocnienie

    Returns:
        True jeśli operacja się powiodła
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Błąd: Plik nie istnieje: {input_file}")
        return False

    if output_file is None:
        # Domyślnie nadpisuj oryginalny plik
        output_path = input_path
    else:
        output_path = Path(output_file)

    return enhance_cad_image(str(input_path), str(output_path),
                             line_thickness, contrast_boost, sharpen, extra_enhance)


def main():
    """Główna funkcja programu z interfejsem CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Poprawia jakość zdjęć CAD - pogrubia linie i zwiększa kontrast.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  python main.py obraz.png                    # Przetwarza plik (nadpisuje oryginalny)
  python main.py obraz.png -o wynik.png       # Przetwarza z określoną nazwą wyjściową
  python main.py -d ./zdjecia -r              # Przetwarza katalog z podkatalogami (nadpisuje)
  python main.py -d ./zdjecia -r -t 5 -c 3.0  # Maksymalna grubość i kontrast
  python main.py -d ./zdjecia -r -e           # Z dodatkowym wzmocnieniem linii
  python main.py -d ./zdjecia -od ./wyniki -r # Zapisuje do osobnego folderu
        """
    )

    parser.add_argument("input", nargs="?", help="Ścieżka do pliku wejściowego PNG")
    parser.add_argument("-o", "--output", help="Ścieżka do pliku wyjściowego")
    parser.add_argument("-d", "--directory", help="Katalog z plikami do przetworzenia")
    parser.add_argument("-od", "--output-dir", help="Katalog na pliki wyjściowe")
    parser.add_argument("-t", "--thickness", type=int, default=4, choices=range(1, 6),
                        help="Grubość pogrubienia linii (1-5, domyślnie: 4)")
    parser.add_argument("-c", "--contrast", type=float, default=2.5,
                        help="Współczynnik kontrastu (domyślnie: 2.5)")
    parser.add_argument("-ns", "--no-sharpen", action="store_true",
                        help="Wyłącz wyostrzanie")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Przetwarzaj podkatalogi rekurencyjnie")
    parser.add_argument("-e", "--extra-enhance", action="store_true",
                        help="Dodatkowe wzmocnienie dla maksymalnej widoczności linii")

    args = parser.parse_args()

    sharpen = not args.no_sharpen

    if args.directory:
        # Tryb przetwarzania katalogu
        success, errors = process_directory(
            args.directory,
            args.output_dir,
            args.thickness,
            args.contrast,
            sharpen,
            args.recursive,
            args.extra_enhance
        )
        print(f"\nZakończono: {success} plików przetworzonych, {errors} błędów.")
        return 0 if errors == 0 else 1

    elif args.input:
        # Tryb pojedynczego pliku
        if process_single_file(args.input, args.output, args.thickness,
                               args.contrast, sharpen, args.extra_enhance):
            print("Przetwarzanie zakończone pomyślnie.")
            return 0
        else:
            print("Wystąpił błąd podczas przetwarzania.")
            return 1

    else:
        parser.print_help()
        print("\n--- Tryb interaktywny ---")
        print("Podaj ścieżkę do pliku lub katalogu z obrazami PNG:")
        user_input = input("> ").strip()

        if not user_input:
            print("Nie podano ścieżki. Kończę.")
            return 1

        path = Path(user_input)

        if path.is_file():
            if process_single_file(str(path), line_thickness=args.thickness,
                                   contrast_boost=args.contrast, sharpen=sharpen):
                print("Przetwarzanie zakończone pomyślnie.")
                return 0
            return 1

        elif path.is_dir():
            success, errors = process_directory(
                str(path), line_thickness=args.thickness,
                contrast_boost=args.contrast, sharpen=sharpen,
                recursive=True  # Domyślnie przeszukuj podkatalogi
            )
            print(f"\nZakończono: {success} plików przetworzonych, {errors} błędów.")
            return 0 if errors == 0 else 1

        else:
            print(f"Błąd: Ścieżka nie istnieje: {user_input}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
