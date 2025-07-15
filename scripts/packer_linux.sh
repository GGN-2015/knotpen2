#!/bin/bash

# 使用 readlink -f 获取脚本的绝对路径（兼容符号链接）
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# 切换到脚本所在目录
cd "$SCRIPT_DIR" || exit
bash clean_history.sh

# 输出当前目录进行验证
cd "../knotpen2"
echo "当前目录: $(pwd)"

# 做 linux 下的打包
pyinstaller -i logo.ico -F --add-data './font/SourceHanSansSC-VF.ttf:./font/' --add-data 'logo.ico:.' test_main.py -n main

# 压缩成压缩包
mkdir dist/knotpen2
cp ../README.md dist/knotpen2/README.md
cp dist/main dist/knotpen2/main
zip -r dist/knotpen2.zip dist/knotpen2/

mv dist/knotpen2.zip dist/knotpen2_linux_x86-64.zip
