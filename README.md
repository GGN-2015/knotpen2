# knotpen2

[中文 README](./README.zh-CN.md)

![](img/sample_1.svg)
![](img/sample_2.svg)

Knotpen2 is a GUI tool for drawing knot and link diagrams and calculating PD_CODE output.

## Quick Start

### Run From Source

1. Install Python dependencies:

```bash
python -m pip install pygame numpy
```

2. Run from the repository root:

```bash
python knotpen2/test_main.py
```

The program automatically downloads `SourceHanSansSC-VF.ttf` on first launch if the font file is missing.

### Run A Packaged Build

Extract the release package and double-click `main.exe`.

## Manuals

Each manual has an English page and a Chinese counterpart.

- [Interface User Manual](./docs/interface-user-manual.md) | [中文](./docs/interface-user-manual.zh-CN.md)
- [Storage File Format Manual](./docs/storage-format.md) | [中文](./docs/storage-format.zh-CN.md)
- [Windows Packaging Guide](./docs/packaging-guide.md) | [中文](./docs/packaging-guide.zh-CN.md)
- [Algorithm Manual](./docs/algorithm-manual.md) | [中文](./docs/algorithm-manual.zh-CN.md)

## Interface Overview

The right side of the window contains all command buttons. The drawing canvas uses mouse operations for direct diagram editing.

- Use **New project**, **Open project**, **Save project**, and **Save as project** at the top of the command panel to manage project folders.
- Use **Move view up**, **Move view down**, **Move view left**, and **Move view right** to pan the diagram.
- Use **Help** to open the in-app help page. Click **Close help** to return to editing.
- Use **Increase window** and **Decrease window** to resize the window. The window is kept within the screen bounds.
- Use **Switch language** to switch between English and Chinese UI text.
- Select a node, then use **Set base node**, **Set direction node**, or **Delete selected**.
- Use **Clear all** to back up and clear the diagram.
- Use **Recover save** to load the latest automatic save from the current project.
- Use **Calculate PD_CODE** to generate the PD_CODE text and SVG outputs in the current project's `answer` folder.

For the full workflow, see the [Interface User Manual](./docs/interface-user-manual.md).

## Build For Windows x86_64

The repository includes [build.py](./build.py), which only supports Windows x86_64 packaging.

```bash
python -m pip install pygame numpy pyinstaller
python build.py
```

The build script downloads the missing font if needed, recompiles translation files, builds a single-file `main.exe`, and writes:

```text
dist/knotpen2_<version>_win32_x86-64.zip
```

For details, see the [Windows Packaging Guide](./docs/packaging-guide.md).

## Error Reports

If the app crashes, open an issue in this GitHub project. Include the error log and reproduction steps.

Error logs are stored in the `error_log` folder next to the executed program.

## Citation

```text
@misc{knotpen2,
  author = {Guo, Guannan},
  title = {Knotpen2: A GUI Based Link PD Notation Calculator},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/GGN-2015/knotpen2},
  note = {Access Date: your access date}
}
```
