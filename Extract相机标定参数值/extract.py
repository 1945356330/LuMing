import json
import re
import pdb

# 读取 JSON 文件并遍历处理
import json
from pathlib import Path
import json

def parse_json_and_extract_info(jsonFile):
    with open(jsonFile, 'r') as json_file:
        parsed_json = json.load(json_file)

    videoNum = len(parsed_json["ai_info"])  # 获取视频段的数量

    result = {}  # 用列表保存所有 (c_value, rpy_value)

    for videoIndex in range(videoNum):
        aiInfo = parsed_json['ai_info']
        frames = aiInfo['frames']  # 获取视频的所有帧

        for frame in frames:
            frame_id = frame.get("frame_id", [])
            frame_pts = frame.get("frame_pts", [])

            infos = frame.get("infos", [])
            if infos:
                for info in infos:
                    group_id = info.get("group_id", None)
                    c_value = None
                    rpy_value = None

                    if group_id == 3:
                        for text in info.get('text', []):
                            t_value = str(text.get('t', ''))

                            if 'RPY_V' in t_value:
                                c_value = t_value
                            elif "RPY" in t_value:
                                rpy_value = t_value
                            elif "Re" in t_value:
                                Re_value = t_value

                        if c_value and rpy_value:
                            result[c_value] = rpy_value,Re_value    #

    return result









if __name__ == '__main__':

    folder_path = Path(r"D:\Datasets\20250415")  # ✅ 转成 Path 对象
    all_results = {}

    for json_file in folder_path.glob("*.json"):
        result = parse_json_and_extract_info(json_file)
        all_results[json_file.name] = result
        print(result)



