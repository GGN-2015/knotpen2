# Interface User Manual

[中文版本](./interface-user-manual.zh-CN.md)

This manual explains how to use Knotpen2 from the graphical interface.

## Window Layout

The window has two functional areas:

- The canvas, where knots and links are drawn.
- The right-side command panel, which contains operation buttons on a rounded background.

Clicks inside the command panel background are treated as UI clicks, even when they do not hit a specific button. This prevents accidental node creation on the canvas.

The window size adapts to the current screen on startup. Use **Increase window** and **Decrease window** to resize it later; the application keeps the window inside the screen bounds.

## Projects

Knotpen2 works with project folders. A project folder contains:

- `project.json`: the current project data.
- `auto_save/`: automatic save snapshots for that project.
- `answer/`: PD_CODE text and SVG outputs for that project.

The project buttons are placed at the top of the right-side command panel:

- **New project** asks you to choose a folder, clears the canvas, and creates `project.json` in that folder.
- **Open project** asks you to choose an existing project folder that already contains `project.json`.
- **Save project** writes the current canvas to the current project's `project.json`.
- **Save as project** asks you to choose another folder, then writes the current canvas as a separate project there.

Folder selection uses the operating system's directory picker. If the selected folder already has a `project.json`, Knotpen2 asks before overwriting it.

## Language And Help

- **Switch language** changes future UI labels and help text between English and Chinese.
- **Help** opens the in-app help page.
- **Close help** closes the help page and returns to editing.

Historical messages already printed in the message area are not retranslated.

## View Movement

Use these buttons to pan all existing diagram points:

- **Move view up**
- **Move view down**
- **Move view left**
- **Move view right**

If no nodes exist, panning has no visible effect.

## Normal Editing Mode

Knotpen2 starts in normal mode.

- Left-click empty canvas space to create a node.
- Drag a node to move it.
- Right-click a node to delete it.
- Right-click an edge to delete it.
- Double-click near the middle of an edge to split it into two connected edges.
- Click a crossing of two edges to switch which edge is drawn above the other.

Nodes whose degree is not exactly 2 are shown with a solid gray fill. These nodes must be fixed before calculating PD_CODE.

## Continuous Creation Mode

Click an existing node to select it. The selected node turns red, and the program enters continuous creation mode.

In this mode:

- Left-click empty space to create a new node and automatically connect it to the selected node.
- The new node becomes the selected red node.
- Click another existing node to close the curve and leave continuous creation mode.
- Click the red selected node, or right-click anywhere outside the command panel, to exit continuous creation mode.
- Click **Delete selected** to delete the selected node and return to normal mode.

## Base And Direction Nodes

Each connected component must have exactly one base node and one direction node before PD_CODE calculation.

To set them:

1. Click a node to select it.
2. Click **Set base node** to mark it as the base node, shown in blue.
3. Click another adjacent node.
4. Click **Set direction node** to mark it as the direction node, shown in green.

The base node and direction node must be adjacent in the same connected component.

## Clear And Recover

- **Clear all** creates an automatic backup first, then clears all diagram data.
- **Recover save** loads the latest automatic save file from the current project.

Automatic saves are stored in the current project's `auto_save` folder.

## PD_CODE Calculation

Before clicking **Calculate PD_CODE**, make sure:

- Every node has exactly two incident edges.
- Every connected component has one base node and one direction node.
- The base node and direction node are adjacent.
- No point has three segments meeting there. The program does not currently check this condition automatically.

When calculation succeeds, output is written under the current project's `answer` folder.

The generated files include:

- A `.txt` file containing the PD_CODE tuple list.
- A `.num.svg` file with arc numbers.
- A `.nonum.svg` file without arc numbers.
- A `.arrow.svg` file with direction arrows.
