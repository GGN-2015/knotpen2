#!/bin/bash

# 使用 readlink -f 获取脚本的绝对路径（兼容符号链接）
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# 切换到脚本所在目录
cd "$SCRIPT_DIR" || exit

# 检查工具是否存在
linux_installer_path=$(which pyinstaller 2>/dev/null)
if [ -z "$linux_installer_path" ]; then
    echo "没有找到 linux 下的打包工具"
    exit 1
fi

# 构建 linux 下的目标文件
rm -rf dist # 删除上次构建的结果
mkdir -p dist

WINEDEBUG=-all wine packer_windows.bat # 使用 WINEDEBUG=-all  禁用 wine 日志
version=$(python get_version.py)
cp ../knotpen2/dist/knotpen2_win32_x86-64.zip dist/knotpen2_${version}_win32_x86-64.zip
