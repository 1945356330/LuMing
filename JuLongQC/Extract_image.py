import os
import shutil
import concurrent.futures

# ==================== 配置部分 ====================

# 目标文件夹路径
TARGET_DIRECTORY = '/luming/H264_parse_tool/JuLong/2024-10-12OUT/truck'  # 替换为您的图片文件夹路径
DEST_DIRECTORY = '/luming/H264_parse_tool/JuLong/2024-10-12OUT/truck_quchong'  # 替换为提取图片保存的目标文件夹

# 要处理的图片文件扩展名（全部小写）
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# 保留图片的间隔数（保留1张）
KEEP_INTERVAL = 1

# 每隔3张提取1张（跳过3张，提取1张）
EXTRACT_INTERVAL = 9

# 是否在提取前进行预览（不执行提取，仅打印将要提取的文件）
DRY_RUN = False

# 每500张图片输出一次进度
PROGRESS_INTERVAL = 500

# =====================================================

def get_sorted_images(directory, extensions):
    """
    获取目录中按字母顺序排序的图片文件列表。
    """
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        return []

    images = [f for f in files if os.path.splitext(f)[1].lower() in extensions]
    images.sort()
    return images

def extract_image(image_path, dest_directory, dry_run=False):
    """
    提取单张图片到目标目录并记录日志。
    """
    try:
        if not dry_run:
            # 复制文件到目标文件夹
            shutil.copy(image_path, dest_directory)
        return image_path  # 返回提取的图片路径
    except Exception as e:
        return None  # 出现错误时返回 None

def extract_images(directory, images, extract_interval=3, dry_run=False, dest_directory=None):
    """
    按照指定的模式提取图片，并使用多进程加速操作。
    """
    total_images = len(images)
    to_extract = []

    # 倒序提取：反转图片列表，从最后一张开始提取
    images.reverse()

    # 按照间隔提取每隔 EXTRACT_INTERVAL 张的图片
    for i in range(0, total_images, extract_interval + 1):
        image_path = os.path.join(directory, images[i])
        to_extract.append(image_path)

    extracted = 0
    extract_counter = 0  # 提取计数器

    # 获取 CPU 核心数并根据需要调整进程数
    max_processes = os.cpu_count() * 4  # 设置进程池大小为 CPU 核心数的 4 倍（可以根据需求调整）
    print(f"使用 {max_processes} 个进程进行并行提取。")

    # 使用 ProcessPoolExecutor 来并行提取图片
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_processes) as executor:
        futures = [executor.submit(extract_image, image_path, dest_directory, dry_run) for image_path in to_extract]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                extracted += 1
                extract_counter += 1
                # 每提取500张图片打印一次
                if extract_counter % PROGRESS_INTERVAL == 0:
                    print(f"已提取 {extract_counter} 张图片...")
            # 如果不干运行模式，每提取一次输出到文件
            if dry_run:
                pass  # 不执行实际提取，仅打印预览

    return extracted

def main():
    directory = TARGET_DIRECTORY
    dest_directory = DEST_DIRECTORY
    extensions = [ext.lower() for ext in IMAGE_EXTENSIONS]
    extract_interval = EXTRACT_INTERVAL
    dry_run = DRY_RUN

    # 验证目录是否存在
    if not os.path.isdir(directory):
        print(f"错误: 目录 {directory} 不存在。")
        return

    if not os.path.isdir(dest_directory):
        print(f"错误: 目标目录 {dest_directory} 不存在，创建中...")
        os.makedirs(dest_directory)

    images = get_sorted_images(directory, extensions)

    if not images:
        print(f"在目录 {directory} 中未找到符合条件的图片。")
        return

    extracted = extract_images(directory, images, extract_interval, dry_run, dest_directory)

    # 如果是干运行模式，打印相关信息
    if dry_run:
        pass  # 不需要额外的输出

    # 提取完成后的反馈
    if not dry_run and extracted > 0:
        print(f"总共提取了 {extracted} 张图片。")

if __name__ == "__main__":
    main()
