import os
import shutil
import sys
import urllib.request
from pathlib import Path

try:
    from . import constant_config
except ImportError:
    import constant_config


FONT_FILENAME = "SourceHanSansSC-VF.ttf"
FONT_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/adobe-fonts/source-han-sans/"
    "release/Variable/TTF/SourceHanSansSC-VF.ttf"
)
MIN_FONT_SIZE = 1024 * 1024
DOWNLOAD_TIMEOUT = 120
CHUNK_SIZE = 1024 * 1024


def _default_download_path() -> Path:
    return Path(constant_config.USER_DATA_DIR) / "font" / FONT_FILENAME


def _unique_paths(paths):
    result = []
    seen = set()
    for path in paths:
        resolved = Path(path).resolve()
        if resolved not in seen:
            result.append(resolved)
            seen.add(resolved)
    return result


def _download_font(target_path: Path):
    target_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target_path.with_suffix(target_path.suffix + ".download")

    if temp_path.exists():
        temp_path.unlink()

    print(f"Font file not found. Downloading {FONT_FILENAME} ...")
    request = urllib.request.Request(
        FONT_DOWNLOAD_URL,
        headers={"User-Agent": "knotpen2"},
    )

    try:
        with urllib.request.urlopen(request, timeout=DOWNLOAD_TIMEOUT) as response:
            with temp_path.open("wb") as fp:
                while True:
                    chunk = response.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    fp.write(chunk)

        if temp_path.stat().st_size < MIN_FONT_SIZE:
            raise OSError("downloaded font file is unexpectedly small")

        os.replace(temp_path, target_path)
        print(f"Font file saved to: {target_path}")
    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def ensure_font_exists(target_path=None, bundled_path=None) -> str:
    bundled_path = Path(bundled_path or constant_config.FONT_TTF)
    target_path = Path(target_path or _default_download_path())
    executable_font_path = Path(constant_config.PROGRAM_EXE_PATH) / "font" / FONT_FILENAME

    for path in _unique_paths([bundled_path, target_path, executable_font_path]):
        if path.is_file():
            return str(path)

    try:
        _download_font(target_path)
    except Exception as exc:
        raise FileNotFoundError(
            f"Cannot find {FONT_FILENAME}, and automatic download failed. "
            f"Please download it from {FONT_DOWNLOAD_URL} and place it at {target_path}."
        ) from exc

    if bundled_path.is_file():
        return str(bundled_path)
    return str(target_path)


def copy_font_to(target_path) -> str:
    font_path = Path(ensure_font_exists())
    target_path = Path(target_path)

    if font_path.resolve() == target_path.resolve():
        return str(font_path)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(font_path, target_path)
    return str(target_path)
