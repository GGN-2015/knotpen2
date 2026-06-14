# knotpen2

[English README](./README.md)

![](img/sample_1.svg)
![](img/sample_2.svg)

Knotpen2 是一个用于绘制扭结与链环图，并计算 PD_CODE 的图形界面工具。

## 快速开始

### 从源码运行

1. 安装 Python 依赖：

```bash
python -m pip install pygame numpy
```

2. 在仓库根目录运行：

```bash
python knotpen2/test_main.py
```

如果缺少 `SourceHanSansSC-VF.ttf` 字体文件，程序会在首次启动时自动下载。

### 运行打包版本

解压发布包后，双击 `main.exe`。

## 手册

每个手册页面都有英文版和中文版。

- [界面使用手册](./docs/interface-user-manual.zh-CN.md) | [English](./docs/interface-user-manual.md)
- [存储文件格式手册](./docs/storage-format.zh-CN.md) | [English](./docs/storage-format.md)
- [Windows 打包指南](./docs/packaging-guide.zh-CN.md) | [English](./docs/packaging-guide.md)
- [项目算法手册](./docs/algorithm-manual.zh-CN.md) | [English](./docs/algorithm-manual.md)

## 界面概览

窗口右侧包含全部命令按钮。画布本身使用鼠标操作进行直接编辑。

- 使用命令面板顶部的 **新建项目**、**打开项目**、**保存项目** 和 **另存为项目** 管理项目文件夹。
- 使用 **上移视图**、**下移视图**、**左移视图**、**右移视图** 平移图形。
- 使用 **帮助** 打开应用内帮助页，再点击 **关闭帮助** 回到编辑界面。
- 使用 **增大窗口** 和 **减小窗口** 调整窗口大小，窗口会被限制在屏幕范围内。
- 使用 **切换语言** 在英文和中文界面之间切换。
- 选中节点后，可以使用 **设为起始点**、**设为方向点** 或 **删除选中点**。
- 使用 **清空全部** 先备份再清空图形。
- 使用 **恢复存档** 读取当前项目最近一次自动保存。
- 使用 **计算 PD_CODE** 在当前项目的 `answer` 文件夹中生成 PD_CODE 文本与 SVG 输出。

完整流程见 [界面使用手册](./docs/interface-user-manual.zh-CN.md)。

## Windows x86_64 打包

仓库包含 [build.py](./build.py)，只支持 Windows x86_64 打包。

```bash
python -m pip install pygame numpy pyinstaller
python build.py
```

打包脚本会自动下载缺失字体、重新编译翻译文件、生成单文件 `main.exe`，并输出：

```text
dist/knotpen2_<version>_win32_x86-64.zip
```

详细说明见 [Windows 打包指南](./docs/packaging-guide.zh-CN.md)。

## 报错信息

如果应用闪退，请在本 GitHub 项目提交 issue，并附上错误日志与复现步骤。

错误日志位于被执行程序同目录下的 `error_log` 文件夹。

## 如何引用

```text
@misc{knotpen2,
  author = {Guo, Guannan},
  title = {Knotpen2: A GUI Based Link PD Notation Calculator},
  year = {2025},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/GGN-2015/knotpen2},
  note = {Access Date: 你的访问日期}
}
```
