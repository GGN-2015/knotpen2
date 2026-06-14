# Windows Packaging Guide

[中文版本](./packaging-guide.zh-CN.md)

This guide explains how to package Knotpen2 for Windows x86_64.

## Supported Target

The supported packaging target is:

- Operating system: Windows
- Architecture: x86_64 / AMD64
- Output executable: `main.exe`
- Output archive: `dist/knotpen2_<version>_win32_x86-64.zip`

The repository does not currently provide a Linux or macOS release build script.

## Requirements

Use 64-bit Python on Windows.

Install runtime and packaging dependencies:

```bash
python -m pip install pygame numpy pyinstaller
```

If you use a Conda environment, activate it first, then install the same dependencies.

## Build Command

Run from the repository root:

```bash
python build.py
```

Optional flags:

- `--skip-i18n`: skip recompiling `.po` files into `.mo` files.
- `--no-clean`: keep previous build folders before packaging.

## What The Build Script Does

`build.py` performs these steps:

1. Verifies that it is running on Windows x86_64 with 64-bit Python.
2. Checks required project files.
3. Reads `APP_VERSION` from `knotpen2/constant_config.py`.
4. Removes previous build output unless `--no-clean` is used.
5. Compiles translation files from `.po` to `.mo`, unless `--skip-i18n` is used.
6. Ensures `SourceHanSansSC-VF.ttf` exists, downloading it if needed.
7. Runs PyInstaller in one-file mode.
8. Assembles a release folder containing:
   - `main.exe`
   - `README.md`
   - `README.zh-CN.md`
   - `docs/`
   - `img/`
   - `i18n/`
9. Verifies that all English and Chinese manual files are present in the release folder.
10. Compresses the release folder into `dist/knotpen2_<version>_win32_x86-64.zip`.
11. Verifies that all English and Chinese manual files are present in the final archive.

## Font Handling

Knotpen2 uses `SourceHanSansSC-VF.ttf`. If it is missing, the build script and runtime code download it from Adobe's Source Han Sans repository on GitHub.

The font is placed at:

```text
knotpen2/font/SourceHanSansSC-VF.ttf
```

The `knotpen2/font/` directory is ignored by Git, so the font is not committed to the repository.

## Translation Handling

Translations live under:

```text
knotpen2/i18n/locales/<lang>/LC_MESSAGES/knotpen2.po
```

The build script compiles them into:

```text
knotpen2/i18n/locales/<lang>/LC_MESSAGES/knotpen2.mo
```

The compiler is implemented in `build.py` and does not require external gettext tools.

## PyInstaller Data Files

The executable bundles:

- `font/SourceHanSansSC-VF.ttf`
- `logo.ico`
- `i18n/`

The release archive also includes `README.md`, `README.zh-CN.md`, `docs/`, and `img/` next to `main.exe`.

The `docs/` directory contains both English and Chinese versions of:

- interface user manual
- storage file format manual
- Windows packaging guide
- project algorithm manual

## Common Failures

### `PyInstaller is required`

Install PyInstaller in the Python environment used for the build:

```bash
python -m pip install pyinstaller
```

### Build fails on non-Windows systems

`build.py` intentionally stops outside Windows x86_64. Build on a Windows x86_64 machine or VM.

### Font download fails

Check network access to GitHub. You may also manually download `SourceHanSansSC-VF.ttf` and place it at:

```text
knotpen2/font/SourceHanSansSC-VF.ttf
```

### The packaged app cannot find translations

Run `python build.py` without `--skip-i18n` so `.mo` files are refreshed and included.
