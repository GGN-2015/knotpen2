# Knotpen2 使用说明

[English version](./RELEASE_README.md)

Knotpen2 是一个用于绘制扭结与链环图，并生成 PD_CODE 输出的桌面软件。

## 启动软件

1. 解压发布压缩包。
2. 保持 `main.exe`、`docs/`、`img/` 和 `i18n/` 位于同一个解压目录中。
3. 双击 `main.exe` 启动 Knotpen2。

软件启动后，左侧是绘图画布，右侧是操作按钮。

## 基本流程

1. 点击 **新建项目** 选择项目文件夹，或者点击 **打开项目** 打开已有项目文件夹。
2. 在画布上绘制图形：
   - 左键点击空白处创建节点。
   - 拖拽节点移动节点。
   - 右键点击节点或边进行删除。
   - 双击边可以拆分边。
   - 点击交叉点可以切换哪条边在上方。
3. 点击节点后，使用 **设为起始点** 和 **设为方向点** 标记每个连通分支。
4. 点击 **计算 PD_CODE**。

计算结果会输出到当前项目的 `answer/` 文件夹。

## 项目文件夹

Knotpen2 的项目是一个文件夹。项目文件夹包含：

- `project.json`：项目主文件。
- `auto_save/`：自动保存快照。
- `answer/`：生成的 PD_CODE 文本和 SVG 文件。

右侧面板顶部提供项目操作按钮：

- **新建项目**
- **打开项目**
- **保存项目**
- **另存为项目**

## 帮助、语言与窗口大小

- 点击 **帮助** 打开应用内帮助页。
- 点击 **切换语言** 在英文和中文界面之间切换。
- 点击 **增大窗口** 或 **减小窗口** 调整窗口大小。

## 数据与日志

对于 Windows 打包版，默认项目、错误日志和运行时下载资源都会保存在 `main.exe` 旁边。

如果软件崩溃，反馈问题时请附上 `error_log/` 目录中的日志文件。

## 更多手册

- [界面使用手册](./docs/interface-user-manual.zh-CN.md) | [English](./docs/interface-user-manual.md)
- [存储文件格式手册](./docs/storage-format.zh-CN.md) | [English](./docs/storage-format.md)
- [项目算法手册](./docs/algorithm-manual.zh-CN.md) | [English](./docs/algorithm-manual.md)
- [Windows 打包指南](./docs/packaging-guide.zh-CN.md) | [English](./docs/packaging-guide.md)
