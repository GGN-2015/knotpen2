#!/bin/bash

# 使用 readlink -f 获取脚本的绝对路径（兼容符号链接）
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# 切换到脚本所在目录
cd "$SCRIPT_DIR" || exit

# 输出当前目录进行验证
echo "当前目录: $(pwd)"

# 清理本地缓存和自动保存
echo "清理本地缓存和自动保存 ..."
bash clean_history.sh

# 生成 zip 打包
echo "正在生成整环境 zip 压缩包 ..."
cd ../..
zip -r knotpen2.zip knotpen2/
