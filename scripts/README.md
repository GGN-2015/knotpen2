# 如何打包

1. 请在 linux 下使用打包命令
2. 确定 emb_python 正确配置
3. 确定 pyinstaller 在 linux 下可用
4. 确定 wine 在 linux 下可用
5. 前往 `knotpen2/constant_config.py` 文件中修改变量 `APP_VERSION` 的值
6. 运行 `bash scripts/packer_all.sh`
7. 打包后的的压缩文件位于 `scripts/dist` 文件夹下
