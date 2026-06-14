import argparse
import ast
import os
import platform
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "knotpen2"
BUILD_DIR = APP_DIR / "build"
PYINSTALLER_DIST_DIR = APP_DIR / "dist"
ROOT_DIST_DIR = ROOT_DIR / "dist"
PACKAGE_DIR = ROOT_DIST_DIR / "knotpen2"
APP_NAME = "main.exe"
ARCHIVE_ARCH = "win32_x86-64"
PACKAGE_ROOT_DOCUMENT_SOURCES = {
    Path("README.md"): Path("RELEASE_README.md"),
    Path("README.zh-CN.md"): Path("RELEASE_README.zh-CN.md"),
}
PACKAGE_ROOT_DOCUMENT_FILES = list(PACKAGE_ROOT_DOCUMENT_SOURCES)
PACKAGE_README_LINK_REPLACEMENTS = {
    "./RELEASE_README.zh-CN.md": "./README.zh-CN.md",
    "./RELEASE_README.md": "./README.md",
}
REQUIRED_MANUAL_DOC_FILES = [
    Path("docs") / "Savings.md",
    Path("docs") / "algorithm-manual.md",
    Path("docs") / "algorithm-manual.zh-CN.md",
    Path("docs") / "interface-user-manual.md",
    Path("docs") / "interface-user-manual.zh-CN.md",
    Path("docs") / "packaging-guide.md",
    Path("docs") / "packaging-guide.zh-CN.md",
    Path("docs") / "storage-format.md",
    Path("docs") / "storage-format.zh-CN.md",
]
REQUIRED_DOCUMENT_FILES = [
    *PACKAGE_ROOT_DOCUMENT_SOURCES.values(),
    *REQUIRED_MANUAL_DOC_FILES,
]


class BuildError(RuntimeError):
    pass


def log(message: str):
    print(f"[build] {message}")


def run_command(command, cwd=None):
    log("running: " + " ".join(str(item) for item in command))
    subprocess.run(command, cwd=cwd, check=True)


def require_windows_x86_64():
    if platform.system() != "Windows":
        raise BuildError("build.py only supports Windows x86_64 packaging.")

    machine = platform.machine().lower()
    is_64bit_python = struct.calcsize("P") * 8 == 64
    if machine not in {"amd64", "x86_64"} or not is_64bit_python:
        raise BuildError("build.py must be run with 64-bit Python on Windows x86_64.")


def read_app_version() -> str:
    config_path = APP_DIR / "constant_config.py"
    for line in config_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("APP_VERSION"):
            return line.split("=", 1)[1].split("#", 1)[0].strip().strip("\"'")
    raise BuildError(f"APP_VERSION not found in {config_path}")


def compile_po_file(po_path: Path, mo_path: Path):
    messages = parse_po_file(po_path)
    mo_path.parent.mkdir(parents=True, exist_ok=True)
    write_mo_file(messages, mo_path)


def parse_po_file(po_path: Path) -> dict[str, str]:
    messages = {}
    current_key = None
    msgid = None
    msgstr = None
    fuzzy = False

    def finish_message():
        nonlocal msgid, msgstr, fuzzy
        if msgid is not None and msgstr is not None and not fuzzy:
            messages[msgid] = msgstr
        msgid = None
        msgstr = None
        fuzzy = False

    with po_path.open("r", encoding="utf-8") as fp:
        for raw_line in fp:
            line = raw_line.strip()

            if not line:
                finish_message()
                current_key = None
                continue

            if line.startswith("#,") and "fuzzy" in line:
                fuzzy = True
                continue

            if line.startswith("#"):
                continue

            if line.startswith("msgid "):
                finish_message()
                current_key = "msgid"
                msgid = ast.literal_eval(line[6:])
                continue

            if line.startswith("msgstr "):
                current_key = "msgstr"
                msgstr = ast.literal_eval(line[7:])
                continue

            if line.startswith('"') and current_key:
                value = ast.literal_eval(line)
                if current_key == "msgid":
                    msgid = (msgid or "") + value
                elif current_key == "msgstr":
                    msgstr = (msgstr or "") + value

    finish_message()
    return messages


def write_mo_file(messages: dict[str, str], mo_path: Path):
    keys = sorted(messages.keys())
    ids = b""
    strs = b""
    offsets = []

    for key in keys:
        msgid = key.encode("utf-8")
        msgstr = messages[key].encode("utf-8")
        offsets.append((len(msgid), len(ids), len(msgstr), len(strs)))
        ids += msgid + b"\0"
        strs += msgstr + b"\0"

    keystart = 7 * 4 + len(keys) * 16
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []

    for msgid_len, msgid_offset, msgstr_len, msgstr_offset in offsets:
        koffsets += [msgid_len, keystart + msgid_offset]
        voffsets += [msgstr_len, valuestart + msgstr_offset]

    output = [
        struct.pack("Iiiiiii", 0x950412DE, 0, len(keys), 7 * 4, 7 * 4 + len(keys) * 8, 0, 0),
        struct.pack(f"{len(koffsets)}i", *koffsets) if koffsets else b"",
        struct.pack(f"{len(voffsets)}i", *voffsets) if voffsets else b"",
        ids,
        strs,
    ]

    with mo_path.open("wb") as fp:
        fp.write(b"".join(output))


def compile_translations():
    locale_dir = APP_DIR / "i18n" / "locales"
    for po_path in locale_dir.glob("*/LC_MESSAGES/knotpen2.po"):
        mo_path = po_path.with_suffix(".mo")
        compile_po_file(po_path, mo_path)
        log(f"compiled {mo_path.relative_to(ROOT_DIR)}")


def find_pyinstaller_command():
    embedded_pyinstaller = ROOT_DIR / "emb_python" / "Scripts" / "pyinstaller.exe"
    if embedded_pyinstaller.is_file():
        return [str(embedded_pyinstaller)]

    try:
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise BuildError(
            "PyInstaller is required. Install it with: python -m pip install pyinstaller"
        ) from exc

    return [sys.executable, "-m", "PyInstaller"]


def ensure_required_files():
    required_files = [
        APP_DIR / "test_main.py",
        APP_DIR / "logo.ico",
        APP_DIR / "i18n" / "locales" / "zh_CN" / "LC_MESSAGES" / "knotpen2.po",
        APP_DIR / "i18n" / "locales" / "en_US" / "LC_MESSAGES" / "knotpen2.po",
        *(ROOT_DIR / path for path in REQUIRED_DOCUMENT_FILES),
    ]

    missing = [path for path in required_files if not path.exists()]
    if missing:
        details = "\n".join(f"  - {path}" for path in missing)
        raise BuildError(f"required build files are missing:\n{details}")


def clean_build_outputs():
    for path in [BUILD_DIR, PYINSTALLER_DIST_DIR, ROOT_DIST_DIR]:
        if path.exists():
            log(f"removing {path.relative_to(ROOT_DIR)}")
            shutil.rmtree(path)


def pyinstaller_add_data_arg(src: str, dst: str) -> str:
    return f"{src}{os.pathsep}{dst}"


def build_executable():
    sys.path.insert(0, str(APP_DIR))
    import font_utils

    font_path = font_utils.copy_font_to(APP_DIR / "font" / font_utils.FONT_FILENAME)
    pyinstaller = find_pyinstaller_command()
    add_data = [
        pyinstaller_add_data_arg(font_path, "font"),
        pyinstaller_add_data_arg(str(APP_DIR / "logo.ico"), "."),
        pyinstaller_add_data_arg(str(APP_DIR / "i18n"), "i18n"),
    ]

    command = [
        *pyinstaller,
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        APP_NAME,
        "--icon",
        str(APP_DIR / "logo.ico"),
    ]

    for item in add_data:
        command.extend(["--add-data", item])

    command.append(str(APP_DIR / "test_main.py"))
    run_command(command, cwd=APP_DIR)

    executable = PYINSTALLER_DIST_DIR / APP_NAME
    if not executable.is_file():
        raise BuildError(f"PyInstaller did not create {executable}")
    return executable


def copy_tree(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))


def copy_release_readme(src: Path, dst: Path):
    text = src.read_text(encoding="utf-8")
    for old, new in PACKAGE_README_LINK_REPLACEMENTS.items():
        text = text.replace(old, new)
    dst.write_text(text, encoding="utf-8", newline="\n")


def assemble_package(executable: Path):
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(executable, PACKAGE_DIR / APP_NAME)
    for output_path, source_path in PACKAGE_ROOT_DOCUMENT_SOURCES.items():
        copy_release_readme(ROOT_DIR / source_path, PACKAGE_DIR / output_path)
    copy_tree(ROOT_DIR / "docs", PACKAGE_DIR / "docs")
    copy_tree(ROOT_DIR / "img", PACKAGE_DIR / "img")
    copy_tree(APP_DIR / "i18n", PACKAGE_DIR / "i18n")


def package_document_files() -> list[Path]:
    docs_dir = ROOT_DIR / "docs"
    docs_files = []
    if docs_dir.is_dir():
        docs_files = [
            path.relative_to(ROOT_DIR)
            for path in sorted(docs_dir.rglob("*.md"))
        ]
    return [*PACKAGE_ROOT_DOCUMENT_FILES, *docs_files]


def verify_packaged_documents():
    missing = [
        PACKAGE_DIR / path
        for path in package_document_files()
        if not (PACKAGE_DIR / path).is_file()
    ]
    if missing:
        details = "\n".join(f"  - {path}" for path in missing)
        raise BuildError(f"packaged documentation files are missing:\n{details}")


def write_zip(version: str) -> Path:
    archive_path = ROOT_DIST_DIR / f"knotpen2_{version}_{ARCHIVE_ARCH}.zip"
    if archive_path.exists():
        archive_path.unlink()

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for path in PACKAGE_DIR.rglob("*"):
            if path.is_file():
                zipf.write(path, path.relative_to(ROOT_DIST_DIR))

    return archive_path


def verify_archive_documents(archive_path: Path):
    expected = {
        (Path(PACKAGE_DIR.name) / path).as_posix()
        for path in package_document_files()
    }
    with zipfile.ZipFile(archive_path, "r") as zipf:
        archived = set(zipf.namelist())

    missing = sorted(expected - archived)
    if missing:
        details = "\n".join(f"  - {path}" for path in missing)
        raise BuildError(f"archive documentation files are missing:\n{details}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build knotpen2 for Windows x86_64 only."
    )
    parser.add_argument(
        "--skip-i18n",
        action="store_true",
        help="Do not recompile .po files into .mo files before packaging.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove previous build/dist directories before packaging.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        require_windows_x86_64()
        ensure_required_files()
        version = read_app_version()

        if not args.no_clean:
            clean_build_outputs()

        if not args.skip_i18n:
            compile_translations()

        executable = build_executable()
        assemble_package(executable)
        verify_packaged_documents()
        archive_path = write_zip(version)
        verify_archive_documents(archive_path)
        log(f"created {archive_path.relative_to(ROOT_DIR)}")
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    except BuildError as exc:
        print(f"[build:error] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
