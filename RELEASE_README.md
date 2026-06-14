# Knotpen2 User README

[中文版本](./RELEASE_README.zh-CN.md)

Knotpen2 is a desktop application for drawing knot and link diagrams and generating PD_CODE outputs.

## Start The App

1. Extract the release zip file.
2. Keep `main.exe`, `docs/`, `img/`, and `i18n/` in the same extracted folder.
3. Double-click `main.exe` to start Knotpen2.

The app opens with the drawing canvas on the left and the command buttons on the right.

## Basic Workflow

1. Click **New project** and choose a project folder, or click **Open project** to open an existing project folder.
2. Draw the diagram on the canvas:
   - Left-click empty space to create a node.
   - Drag a node to move it.
   - Right-click a node or edge to delete it.
   - Double-click an edge to split it.
   - Click a crossing to switch which edge is above.
3. Click a node and use **Set base node** and **Set direction node** to mark each connected component.
4. Click **Calculate PD_CODE**.

Calculation outputs are written to the current project's `answer/` folder.

## Project Folders

A Knotpen2 project is a folder. It contains:

- `project.json`: the main project file.
- `auto_save/`: automatic save snapshots.
- `answer/`: generated PD_CODE text and SVG files.

Use the project buttons at the top of the right-side panel:

- **New project**
- **Open project**
- **Save project**
- **Save as project**

## Help, Language, And Window Size

- Click **Help** to open the in-app help page.
- Click **Switch language** to switch between English and Chinese UI text.
- Click **Increase window** or **Decrease window** to change the window size.

## Data And Logs

For the packaged Windows app, default projects, error logs, and downloaded runtime assets are stored next to `main.exe`.

If the app crashes, include the files under `error_log/` when reporting the problem.

## More Manuals

- [Interface User Manual](./docs/interface-user-manual.md) | [中文](./docs/interface-user-manual.zh-CN.md)
- [Storage File Format Manual](./docs/storage-format.md) | [中文](./docs/storage-format.zh-CN.md)
- [Project Algorithm Manual](./docs/algorithm-manual.md) | [中文](./docs/algorithm-manual.zh-CN.md)
- [Windows Packaging Guide](./docs/packaging-guide.md) | [中文](./docs/packaging-guide.zh-CN.md)
