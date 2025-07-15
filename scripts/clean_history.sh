#!/bin/bash

# 使用 readlink -f 获取脚本的绝对路径（兼容符号链接）
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# 切换到脚本所在目录
cd "$SCRIPT_DIR" || exit

rm -rf ../knotpen2/answer/*
rm -rf ../knotpen2/error_log/*
rm -rf ../knotpen2/auto_save/*

# 删除构建的所有 pyc
rm -rf ../knotpen2/__pycache__/*.pyc
rm -rf ../knotpen2/build
rm -rf ../knotpen2/dist
