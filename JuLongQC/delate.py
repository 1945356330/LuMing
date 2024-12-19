import os

# ==================== 配置部分 ====================

# 目标文件夹路径
TARGET_DIRECTORY = '/luming/H264_parse_tool/JuLong/2024-10-12OUT/truck'  # 替换为您的图片文件夹路径

# 删除记录文件的路径
DELETE_LOG_FILE = '/luming/H264_parse_tool/JuLong/2024-10-12OUT/delete_log.txt'  # 替换为删除日志文件路径

# 要处理的图片文件扩展名（全部小写）
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

# 保留图片的间隔数（保留1张）
KEEP_INTERVAL = 1

# 每次保留后删除的图片数量（删除3张）
DELETE_COUNT = 2

# 是否在删除前进行预览（不执行删除，仅打印将要删除的文件）
DRY_RUN = False

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

def delete_images(directory, images, keep_interval=1, delete_count=3, dry_run=False, log_file=None):
    """
    按照指定的模式删除图片，并记录删除操作。
    """
    total_images = len(images)
    indices_to_keep = set()

    # 计算要保留的图片索引
    i = 0
    while i < total_images:
        indices_to_keep.add(i)
        i += keep_interval + delete_count

    deleted = 0
    to_delete = []
    delete_counter = 0  # 删除计数器

    for idx, image in enumerate(images):
        if idx not in indices_to_keep:
            image_path = os.path.join(directory, image)
            to_delete.append(image_path)

    if dry_run:
        # 仅在干运行模式下才显示要删除的文件
        for path in to_delete:
            pass  # 在此仅做预览，无需打印
    else:
        for path in to_delete:
            try:
                os.remove(path)
                deleted += 1
                delete_counter += 1
                # 每删除500张图片打印一次
                if delete_counter % 500 == 0:
                    print(f"已删除 {delete_counter} 张图片...")
                # 记录删除日志
                if log_file:
                    with open(log_file, 'a') as f:
                        f.write(f"{os.path.basename(path)}\n")
            except Exception as e:
                pass  # 在删除失败时不打印错误

    return deleted

def main():
    directory = TARGET_DIRECTORY
    extensions = [ext.lower() for ext in IMAGE_EXTENSIONS]
    keep_interval = KEEP_INTERVAL
    delete_count = DELETE_COUNT
    dry_run = DRY_RUN
    log_file = DELETE_LOG_FILE

    # 验证目录是否存在
    if not os.path.isdir(directory):
        return

    images = get_sorted_images(directory, extensions)

    if not images:
        return

    deleted = delete_images(directory, images, keep_interval, delete_count, dry_run, log_file)

    # 如果是干运行模式，打印相关信息
    if dry_run:
        pass  # 不需要额外的输出

    # 删除完成后的反馈
    if not dry_run and deleted > 0:
        print(f"总共删除了 {deleted} 张图片，删除记录已保存到 {log_file}。")

if __name__ == "__main__":
    main()
