# knotpen2

![](img/sample_1.svg)
![](img/sample_2.svg)

扭结与链环的绘制、PD_CODE 计算工具。

Knot and link diagram editor with PD_CODE calculation.

## 操作指南

### 启动软件

- 源码运行：安装依赖后，在仓库根目录执行 `python knotpen2/test_main.py`。
- 打包版本运行：解压发布包后，双击 `main.exe`。
- 程序右侧会显示操作按钮，原来主要依赖键盘的功能现在都可以通过点击按钮完成。

### 视角移动

- 点击右侧的 **上移视图**、**下移视图**、**左移视图**、**右移视图** 按钮移动屏幕位置。
- 屏幕上没有节点时，移动视图不会产生可见效果。

### 语言切换

- 点击右侧的 **切换语言** 按钮在英文和中文之间切换。
- 已经显示在消息区里的历史文字不会重新翻译。

### 帮助与窗口大小

- 点击右侧的 **帮助** 按钮会打开帮助页面，再次点击 **关闭帮助** 可以回到编辑界面。
- 帮助页面支持中文和英文，会跟随 **切换语言** 按钮变化。
- 点击 **增大窗口** 或 **减小窗口** 可以调整窗口大小，窗口会自动限制在屏幕范围内。

### 节点创建

- 打开软件时，操作模式默认为普通模式。
  - 普通模式下，使用**鼠标左键单击**创建节点。
  - 使用**鼠标右键单击**可以删除节点和边。
  - **双击边的中点**可以对边进行细分，将原来的一条边拆分成两条相连边。
  - **鼠标按住拖拽**可以移动已经创建的节点的位置。
  - **点击线段交叉点**可以切换相交线段的上下位置关系。
    - 反直觉提醒：由于交叉点的换序是线段与线段之间的关系。
    - 每当移动节点位置之后，请务必重新检查所有交叉点的前后关系是否符合预期。
  - 度不等于 2 的节点会使用实心灰色高亮显示。

- 点击节点，使其变成红色，从而进入连续创建模式。
  - 连续创建模式下，左键连续点击空白处可以连续创建节点，并自动和上一个创建的节点连边。
  - 连续创建模式下，点击右侧的 **删除选中点** 按钮可以删除当前选中的节点，并回到普通模式。
  - 左键点击红色的节点，或者右键点击任意位置可以退出连续创建模式。
  - 在连续创建模式下，点击现有的节点，可以将曲线闭合并自动退出连续创建模式。
  - 连续模式下，点击右侧的 **设为起始点** 按钮确定起始点，起始点使用蓝色表示。
  - 连续模式下，点击右侧的 **设为方向点** 按钮确定方向点，方向点不能与起始点重合，方向点使用绿色表示。

- 点击右侧的 **清空全部** 按钮会先自动备份，然后清空所有数据。
  - 如果你不小心清空了所有数据，可以点击 **恢复存档** 按钮恢复上一次自动保存的数据。

### 计算 PD_CODE

- 本程序采用的 PD_CODE 定义详见：https://katlas.org/wiki/Planar_Diagrams

- 在计算 PD_CODE 前，你需要保证：
  - 扭结中没有三线共点。这一点目前版本的程序并不提供检查，请人工保证。
  - 扭结中每个节点都有且仅有两条出边。
  - 每一个连通分支都恰有一个起始点和一个方向点，且起始点和方向点必须相邻。
- 如果出现了上述情况，程序会在计算扭结 PD_CODE 时向用户报错并告知出错原因。

- 如果扭结图中没有以上问题，点击右侧的 **计算 PD_CODE** 按钮，程序会输出一些图片以及一个文本文件。
  - 文本文件中会以四元组的形式输出一个 `pd_code`。
  - 文本文件以及 SVG 图片文件会被存储到可执行文件同目录下的 `answer` 文件夹中。
  - 程序会生成三个 SVG 文件：
    - 一个是 `.num.svg` 结尾的，带有 PD_CODE 中的弧线编号信息。
    - 一个是 `.nonum.svg` 结尾的，不带有 PD_CODE 中的弧线编号信息。
    - 一个是 `.arrow.svg` 结尾的，不带有 PD_CODE 中的弧线编号信息，但带有方向信息。

## English Guide

### Start

- Source run: install dependencies, then run `python knotpen2/test_main.py` from the repository root.
- Packaged run: extract the release package, then double-click `main.exe`.
- Operation buttons are shown on the right side of the window. Features that previously depended on keyboard shortcuts can now be triggered by clicking those buttons.

### Move View

- Click **Move view up**, **Move view down**, **Move view left**, and **Move view right** to move the diagram view.
- If there are no nodes on screen, moving the view has no visible effect.

### Switch Language

- Click **Switch language** to switch between Chinese and English.
- Existing messages already printed in the message area are not retranslated.

### Help And Window Size

- Click **Help** to open the help page, then click **Close help** to return to editing.
- The help page supports both Chinese and English and follows **Switch language**.
- Click **Increase window** or **Decrease window** to resize the window. The window is kept within the screen bounds automatically.

### Create And Edit Nodes

- The program starts in normal mode.
  - In normal mode, left-click an empty area to create a node.
  - Right-click a node or edge to delete it.
  - Double-click the middle of an edge to split it into two connected edges.
  - Drag an existing node to move it.
  - Click an edge crossing to switch which segment is drawn over the other.
    - This ordering belongs to the pair of segments at the crossing.
    - After moving nodes, recheck every crossing order manually.
  - Nodes whose degree is not 2 are highlighted with a solid gray fill.

- Click a node to turn it red and enter continuous creation mode.
  - In continuous creation mode, left-click empty space to keep creating nodes, each automatically connected to the previous node.
  - Click **Delete selected** to delete the selected node and return to normal mode.
  - Click the red node with the left mouse button, or right-click anywhere, to exit continuous creation mode.
  - Click an existing node in continuous creation mode to close the curve and exit the mode.
  - Click **Set base node** to mark the selected node as the base node. Base nodes are shown in blue.
  - Click **Set direction node** to mark the selected node as the direction node. It must not be the same as the base node, and is shown in green.

- Click **Clear all** to create an automatic backup and then clear all data.
  - If you clear data by mistake, click **Recover save** to load the last automatic save.

### Calculate PD_CODE

- The PD_CODE definition used by this program is documented at https://katlas.org/wiki/Planar_Diagrams

- Before calculating PD_CODE, make sure:
  - The knot has no point where three segments meet. The current version does not check this automatically.
  - Every node has exactly two incident edges.
  - Every connected component has exactly one base node and one direction node, and those two nodes are adjacent.
- If these requirements are not satisfied, the program reports the error reason during PD_CODE calculation.

- If the diagram is valid, click **Calculate PD_CODE**. The program outputs images and a text file.
  - The text file contains the `pd_code` as tuples.
  - The text file and SVG files are stored in the `answer` folder next to the executable.
  - The program generates three SVG files:
    - `.num.svg`: includes PD_CODE arc numbers.
    - `.nonum.svg`: does not include PD_CODE arc numbers.
    - `.arrow.svg`: includes direction information.

## 报错信息 / Error Reports

- 如果遇到了应用闪退等问题，可以在本 GitHub 项目上提交 issue。
- 报错时请提供相关错误日志与错误复现流程，日志文件位于可执行文件同目录的 `error_log` 文件夹。
- If the app crashes, please open an issue in this GitHub project.
- Include the error log and reproduction steps. Error logs are stored in the `error_log` folder next to the executable.

## 开发手册 / Development

- 存储结构 / Storage structure: [Savings.md](./docs/Savings.md)

## Windows x86_64 打包 / Windows x86_64 Build

- 打包脚本只支持 Windows x86_64。
- 安装运行依赖和 PyInstaller，例如：`python -m pip install pygame numpy pyinstaller`。
- 在仓库根目录运行：`python build.py`。
- 脚本会自动下载缺失的 `SourceHanSansSC-VF.ttf` 字体文件，重新编译翻译文件，生成单文件 `main.exe`，并输出 `dist/knotpen2_<version>_win32_x86-64.zip`。

- The build script supports Windows x86_64 only.
- Install runtime dependencies and PyInstaller, for example: `python -m pip install pygame numpy pyinstaller`.
- Run from the repository root: `python build.py`.
- The script automatically downloads the missing `SourceHanSansSC-VF.ttf` font, recompiles translations, builds `main.exe`, and writes `dist/knotpen2_<version>_win32_x86-64.zip`.

## 如何引用 / Citation

```text
@misc{knotpen2,
  author = {Guo, Guannan},
  title = {Knotpen2: A GUI Based Link PD Notation Calculator},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/GGN-2015/knotpen2},
  note = {Access Date: your access date / 你的访问日期}
}
```
