# ImprovePhoto - CAD Thumbnail Quality Improvement Tool

A tool for improving the quality of structural component thumbnail images exported from CAD Inventor.
It thickens black lines on a white background for better visibility in PDF documents.

## Requirements

- Python 3.12 or newer
- Required packages: opencv-python, numpy, Pillow (automatically installed from requirements.txt)

## Installation

Packages should already be installed. To reinstall if needed:

```batch
C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```

## Usage

### Method 1: Using the run.bat script (RECOMMENDED)

The easiest way to run the program is with the provided `run.bat` script:

```batch
run.bat -d "path\to\directory" -r
```

### Method 2: Running Python directly

```batch
C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe main.py [options]
```

## Program Options

- `input` - Path to a single PNG file to process
- `-o`, `--output` - Path to the output file
- `-d`, `--directory` - Directory containing files to process
- `-od`, `--output-dir` - Output directory for processed files (if not provided, originals are overwritten)
- `-t`, `--thickness` - Line thickening amount (1–5, default: 4)
- `-c`, `--contrast` - Contrast factor (default: 2.5)
- `-ns`, `--no-sharpen` - Disable sharpening
- `-r`, `--recursive` - Process subdirectories recursively
- `-e`, `--extra-enhance` - Additional enhancement for MAXIMUM line visibility

## Usage Examples

### Process a single file (overwrite original):
```batch
run.bat image.png
```

### Process a single file (keep original):
```batch
run.bat image.png -o image_improved.png
```

### Process an entire directory (overwrite files in place):
```batch
run.bat -d "X:\0.0.0.0 COMPONENT THUMBNAILS" -r
```

### Process with maximum line visibility:
```batch
run.bat -d "X:\0.0.0.0 COMPONENT THUMBNAILS" -r -e
```

### Process with custom parameters:
```batch
run.bat -d ".\photos" -r -t 5 -c 3.0 -e
```
(Maximum line thickness: 5, high contrast: 3.0, extra enhancement)

### Process to a separate output directory (preserves originals):
```batch
run.bat -d ".\photos" -od ".\photos_improved" -r
```

## How It Works

The program performs the following operations:

1. **Load image** - Supports PNG with transparency and special characters in the file path
2. **Convert to grayscale** - Prepares the image for analysis
3. **Increase contrast** - Initial enhancement of the difference between lines and background
4. **Adaptive binarization** - Detects lines of varying intensity (2 methods combined)
5. **Line thickening** - Morphological dilation with configurable parameters
6. **Extra enhancement** (option `-e`):
   - Additional dilation to smooth lines
   - Morphological closing — connects broken lines
7. **CLAHE contrast enhancement** - Adaptive normalization
8. **Sharpening** - Kernel sharpening for better edge clarity
9. **Save with compression** - PNG with maximum compression for smaller file sizes

## Troubleshooting

### Error: "Cannot load image"
- Check that the file path is correct
- Make sure the file is in PNG format
- Verify that you have read permissions for the file

### Lines are too thin
Use the `-e` (extra-enhance) option for maximum visibility:
```batch
run.bat -d "directory" -r -e
```

Or increase the thickness parameter to 5:
```batch
run.bat -d "directory" -r -t 5
```

### Lines are too thick
Decrease the thickness parameter:
```batch
run.bat -d "directory" -r -t 2
```

### Python not found
Make sure Python 3.13 is installed at:
`C:\Users\User\AppData\Local\Programs\Python\Python313\`

## Notes

- By default, the program **overwrites the original files** — make sure you have a backup, or use the `-od` option to save to a separate directory
- The `-r` (recursive) option searches all subdirectories
- The program processes PNG files only
- Alpha channel (transparency) is preserved if present

## License

Copyright © Jakub Balcerzak. All rights reserved.

