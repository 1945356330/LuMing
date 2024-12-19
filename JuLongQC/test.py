#!/usr/bin/env python3
from pathlib import Path
import sys
import io
def count_files(directory: Path, recursive: bool = False) -> int:
    """
    计数指定目录中的文件数量。

    :param directory: 要计数的目录路径
    :param recursive: 是否递归计数子目录中的文件
    :return: 文件数量
    """
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if recursive:
        return sum(1 for _ in directory.rglob('*') if _.is_file())
    else:
        return sum(1 for _ in directory.iterdir() if _.is_file())

def main():
    # 设置目标文件夹的路径
    directory_path = "/luming/H264_parse_tool/JuLong/2024-10-13OUT/truck"  # 请将此路径修改为你要计数的文件夹路径

    # 是否递归计数子目录中的文件
    recursive_count = False  # 将其设置为 False 以仅计数顶层目录中的文件

    dir_path = Path(directory_path)

    # 检查路径是否存在
    if not dir_path.exists():
        print(f"错误：路径 '{dir_path}' 不存在。")
        return

    # 检查路径是否为目录
    if not dir_path.is_dir():
        print(f"错误：'{dir_path}' 不是一个目录。")
        return

    # 计数文件
    total_files = count_files(dir_path, recursive_count)
    print(f"目录 '{dir_path}' 中的文件数量：{total_files}")

if __name__ == "__main__":
    main()
