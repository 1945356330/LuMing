import os
from imagededup.methods import PHash
import logging
from tqdm import tqdm  # 导入 tqdm

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def get_kept_images(input_dir, max_distance=10):
    """
    在指定文件夹中获取保留的图像路径，并返回这些路径。
    """
    phasher = PHash()

    # 生成所有图像的编码
    encodings = phasher.encode_images(image_dir=input_dir)

    # 查找重复项，设置更高的 max_distance 以删除更多重复图像
    duplicates = phasher.find_duplicates(encoding_map=encodings, max_distance_threshold=max_distance)

    processed_images = set()
    kept_images = []  # 收集所有保留的图像路径

    for original_image, duplicate_images in duplicates.items():
        if original_image in processed_images:
            continue

        processed_images.add(original_image)
        kept_images.append(os.path.join(input_dir, original_image))  # 保留原始图像

        for duplicate_image in duplicate_images:
            if duplicate_image not in processed_images:
                processed_images.add(duplicate_image)

    logging.info(f"Found {len(kept_images)} images to keep in folder: {input_dir}")
    return kept_images

def save_kept_images_to_txt(kept_images, output_txt_path):
    """
    将保留的图像路径写入文本文件，并显示写入进度。
    """
    try:
        with open(output_txt_path, 'w') as txt_file:
            # 使用 tqdm 显示进度条
            for image in tqdm(kept_images, desc="Writing kept images", unit="image"):
                txt_file.write(f"{image}\n")
        logging.info(f"Kept images have been written to {output_txt_path}")
    except Exception as e:
        logging.error(f"Error writing to {output_txt_path}: {e}")

def process_directory(input_dir, output_txt_path=None, max_distance=10):
    """
    处理指定文件夹中的图像，获取保留的图像路径并保存到文本文件。
    """
    logging.info(f"Processing folder: {input_dir}")

    # 获取保留图像路径
    kept_images = get_kept_images(input_dir, max_distance)

    # 将保留的图像路径保存到文本文件
    if output_txt_path:
        save_kept_images_to_txt(kept_images, output_txt_path)

if __name__ == "__main__":
    # 示例用法：
    input_dir = '/luming/H264_parse_tool/JuLong/2024-10-13OUT/car_out'  # 指定的图像文件夹路径
    output_txt_path = '/luming/H264_parse_tool/JuLong/2024-10-13OUT/car_kept_images_out1.txt'  # 自定义输出路径

    max_distance = 17  # 设置更高的 max_distance 以删除更多重复图像

    process_directory(input_dir, output_txt_path, max_distance)
