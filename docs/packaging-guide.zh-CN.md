# Windows 打包指南

[English version](./packaging-guide.md)

本文说明如何为 Windows x86_64 打包 Knotpen2。

## 支持目标

当前支持的打包目标是：

- 操作系统：Windows
- 架构：x86_64 / AMD64
- 输出可执行文件：`main.exe`
- 输出压缩包：`dist/knotpen2_<version>_win32_x86-64.zip`

仓库目前不提供 Linux 或 macOS 发布构建脚本。

## 环境要求

请在 Windows 上使用 64 位 Python。

安装运行和打包依赖：

```bash
python -m pip install pygame numpy pyinstaller
```

如果使用 Conda 环境，请先激活环境，再安装同样的依赖。

## 打包命令

在仓库根目录运行：

```bash
python build.py
```

可选参数：

- `--skip-i18n`：跳过将 `.po` 编译为 `.mo`。
- `--no-clean`：打包前不删除上一次构建目录。

## 打包脚本流程

`build.py` 会执行以下步骤：

1. 确认当前是 Windows x86_64，并使用 64 位 Python。
2. 检查必要项目文件。
3. 从 `knotpen2/constant_config.py` 读取 `APP_VERSION`。
4. 删除旧构建输出，除非使用了 `--no-clean`。
5. 将 `.po` 翻译文件编译为 `.mo`，除非使用了 `--skip-i18n`。
6. 确保 `SourceHanSansSC-VF.ttf` 字体存在，缺失时自动下载。
7. 使用 PyInstaller 以单文件模式构建。
8. 组装发布目录，包含：
   - `main.exe`
   - `README.md`
   - `README.zh-CN.md`
   - `docs/`
   - `img/`
   - `i18n/`
9. 校验发布目录中是否包含全部英文和中文手册文件。
10. 将发布目录压缩为 `dist/knotpen2_<version>_win32_x86-64.zip`。
11. 校验最终压缩包中是否包含全部英文和中文手册文件。

## 字体处理

Knotpen2 使用 `SourceHanSansSC-VF.ttf`。如果字体缺失，打包脚本和运行时代码都会从 GitHub 上 Adobe Source Han Sans 仓库下载它。

字体保存到：

```text
knotpen2/font/SourceHanSansSC-VF.ttf
```

`knotpen2/font/` 目录被 Git 忽略，因此字体文件不会提交到仓库。

## 翻译文件处理

翻译源文件位于：

```text
knotpen2/i18n/locales/<lang>/LC_MESSAGES/knotpen2.po
```

打包脚本会将其编译为：

```text
knotpen2/i18n/locales/<lang>/LC_MESSAGES/knotpen2.mo
```

编译逻辑在 `build.py` 内部实现，不依赖外部 gettext 工具。

## PyInstaller 数据文件

可执行文件会打包：

- `font/SourceHanSansSC-VF.ttf`
- `logo.ico`
- `i18n/`

发布压缩包还会把 `README.md`、`README.zh-CN.md`、`docs/` 和 `img/` 放在 `main.exe` 旁边。

`docs/` 目录包含以下内容的英文和中文版本：

- 界面使用手册
- 存储文件格式手册
- Windows 打包指南
- 项目算法手册

## 常见问题

### `PyInstaller is required`

请在用于打包的 Python 环境中安装 PyInstaller：

```bash
python -m pip install pyinstaller
```

### 非 Windows 系统打包失败

`build.py` 会主动拒绝非 Windows x86_64 环境。请在 Windows x86_64 机器或虚拟机中打包。

### 字体下载失败

检查是否能访问 GitHub。也可以手动下载 `SourceHanSansSC-VF.ttf`，放到：

```text
knotpen2/font/SourceHanSansSC-VF.ttf
```

### 打包后的应用找不到翻译

不带 `--skip-i18n` 运行 `python build.py`，让脚本刷新并打包 `.mo` 文件。
