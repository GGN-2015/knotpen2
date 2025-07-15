import argparse
import os
import zipfile
from pathlib import Path


def compress_file(input_path):
    """将输入的文件或文件夹压缩为 ZIP 文件"""
    input_path = Path(input_path)
    
    # 检查输入路径是否存在
    if not input_path.exists():
        print(f"错误：路径不存在 - {input_path}")
        return
    
    # 确定输出路径（在同一目录下，文件名后添加 .zip）
    if input_path.is_file():
        output_path = input_path.parent / f"{input_path.stem}.zip"
    else:
        output_path = input_path.parent / f"{input_path.name}.zip"
    
    try:
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if input_path.is_file():
                # 压缩单个文件
                zipf.write(input_path, arcname=input_path.name)
                print(f"已压缩文件：{input_path} -> {output_path}")
            else:
                # 压缩文件夹及其内容
                for root, dirs, files in os.walk(input_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(input_path.parent)
                        zipf.write(file_path, arcname=arcname)
                print(f"已压缩文件夹：{input_path} -> {output_path}")
    except Exception as e:
        print(f"压缩过程中出错：{e}")


def main():
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="将文件或文件夹压缩为 ZIP 文件")
    parser.add_argument("path", help="要压缩的文件或文件夹路径")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 执行压缩操作
    compress_file(args.path)


if __name__ == "__main__":
    main()    
