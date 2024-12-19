import os
import shutil
import logging

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def extract_files_from_txt(txt_file_path, source_dir, target_dir):
    """
    从 txt 文件中提取指定的文件，并将其从源目录复制到目标目录。
    
    :param txt_file_path: 包含文件路径的 txt 文件路径
    :param source_dir: 源目录，包含待提取的文件
    :param target_dir: 目标目录，提取的文件将被复制到这里
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logging.info(f"Created target directory: {target_dir}")

    # 读取 txt 文件中的每行路径
    try:
        with open(txt_file_path, 'r') as file:
            file_paths = file.readlines()
            logging.info(f"Read {len(file_paths)} file paths from {txt_file_path}")
    except Exception as e:
        logging.error(f"Error reading the txt file {txt_file_path}: {e}")
        return

    # 复制文件
    total_files = len(file_paths)
    counter = 0  # 用于计数每处理多少文件打印一次

    for file_path in file_paths:
        file_path = file_path.strip()  # 移除路径中的空白字符
        if os.path.isabs(file_path):  # 如果路径是绝对路径，直接检查
            source_file = file_path
        else:  # 如果是相对路径，根据源目录组合成完整路径
            source_file = os.path.join(source_dir, file_path)

        if os.path.exists(source_file):
            try:
                # 获取目标文件路径
                target_file = os.path.join(target_dir, os.path.basename(source_file))
                shutil.copy(source_file, target_file)
                
                # 更新计数器
                counter += 1

                # 每处理500个文件打印一次
                if counter % 500 == 0 or counter == total_files:
                    logging.info(f"Processed {counter}/{total_files} files.")

            except Exception as e:
                logging.error(f"Error copying {source_file} to {target_file}: {e}")
        else:
            logging.warning(f"File not found: {source_file}")

if __name__ == "__main__":
    # 示例用法：
    txt_file_path = '/luming/H264_parse_tool/JuLong/2024-10-13OUT/car_kept_images_out1.txt'  # 包含文件路径的 txt 文件
    source_dir = '/luming/H264_parse_tool/JuLong/2024-10-13OUT/car_out'  # 源目录
    target_dir = '/luming/H264_parse_tool/JuLong/2024-10-13OUT/car_out1'  # 目标目录（提取的文件将被复制到这里）

    extract_files_from_txt(txt_file_path, source_dir, target_dir)


