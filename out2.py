import json
import re
import pdb
import pdb
# 读取 JSON 文件并遍历处理
def parse_json_and_extract_info(jsonFile):
    with open(jsonFile, 'r') as json_file:
        parsed_json = json.load(json_file)

    videoNum = len(parsed_json["ai_info"])  # 获取视频段的数量

    # 提取外层字段数据
    extracted_data_group_18 = []
    extracted_data_group_3 = []
    extracted_data_other = []
    # extracted_data_group4 = []
    extracted_data = []
    for videoIndex in range(videoNum):
        aiInfo = parsed_json['ai_info']
        frames = aiInfo['frames']  # 获取视频的所有帧

        # 遍历每一帧数据
        for frame in frames:
            frame_id = frame.get("frame_id", [])
            # pdb.set_trace()
            # if frame_id == 0:
            #     print("if frame_id == 0 所在 group_id",group_id)
            frame_pts = frame.get("frame_pts", [])
            # print(frame_id)
            # 如果有 frame_id 和 frame_pts，就按需求保存
            if frame_id is not None:
                extracted_data_group_18.append({"frame_id": frame_id})
            # if frame_id == 0:
            #     extracted_data_group_18.append({"frame_id": frame_id})
                if frame_pts:
                    extracted_data_group_18.append({"frame_pts": frame_pts})

                infos = frame.get("infos", [])
                if infos:
                    for info in infos:
                        group_id = info.get("group_id", None)

                        # group_id == 18
                        group_id18 = ["H", "CW", "LM", "HL", 'MV', "mv3", "Pt", 'Ba', 'Ac', 'vp']
                        group_id3 = ["VP", 'Ba', 'Ac', 'vp']
                        group_idNone = ["H", "LM", "HL", "mv3", "Pt",'Ba','Ac','vp']
                        if group_id == 18:
                            for text in info.get('text', []):
                                t_value = str(text.get('t', ''))
                                calib_data = {}
                                for key in  group_id18:
                                    keyFind = key + ':'
                                    if t_value.startswith(keyFind):  # Ensure t_value starts with the key
                                        calib_data[key] = t_value.split(':')[1]
                                if calib_data:
                                    extracted_data_group_18.append(calib_data)

                            continue

                        # group_id == 3

                        elif group_id == 3:
                            for text in info.get('text', []):
                                t_value = str(text.get('t', ''))
                                calib_data = {}
                                for key in group_id3:
                                    keyFind = key + ':'
                                    if t_value.startswith(keyFind):
                                        calib_data[key] = t_value.split(':')[1]
                                if "VP" in calib_data:
                                    vp_value = calib_data["VP"]

                                    # 检查是否包含括号，如果有括号则舍去该值
                                    if '(' in vp_value and ')' in vp_value:
                                        calib_data["VP"] = None  # 或者删除该字段 calib_data.pop("VP", None)
                                if calib_data:
                                    extracted_data_group_3.append(calib_data)

                            continue


                        elif group_id is not None:
                            for text in info.get('text', []):
                                t_value = str(text.get('t', ''))
                                calib_data = {}
                                for key in group_idNone:
                                    keyFind = key + ':'
                                    if t_value.startswith(keyFind):
                                        calib_data[key] = t_value.split(':')[1]
                                if calib_data:
                                    extracted_data_other.append(calib_data)
            else:
                pass

    extracted_data = extracted_data_group_18


    return extracted_data
import os
def process_data(data, outer_fields=None, inner_fields=None, input_file=None):
    outer_fields = outer_fields or ["H", "CW", "LM", "HL", "Pt"]
    inner_fields = inner_fields or ["MV", "mv1", "mv3", 'Ba', 'Ac', 'vp', 'frame_id', "frame_pts"]

    output = []  # 存储最终输出
    current_outer = {field: None for field in outer_fields}  # 当前外层字段
    current_object = []  # 当前对象列表
    last_ew_values = {}  # 存储上次的外层值，用于检测变化

    # 存储 mv_values、frame_id 和 frame_pts 的数组
    all_mv_values = []

    # 存储frame_id, frame_pts, MV的中间状态
    frame_id_values = []
    frame_pts_values = []
    mv_values = []
    # 获取文件名（去掉扩展名）
    import os

    if input_file:
        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        video_name = f"{base_filename}.mp4"
        json_name = f"{base_filename}.json"
    else:
        video_name = ""
        json_name = ""

    # 遍历每个输入项
    for item in data:
        # 处理 "frame_id" 字段
        if "frame_id" in item:
            frame_id_value = item["frame_id"]
            if isinstance(frame_id_value, str):
                frame_id_values += frame_id_value.split(":")[-1].split("/")  # 拆分并添加到 frame_id_values
            elif isinstance(frame_id_value, int):
                frame_id_values.append(str(frame_id_value))  # 如果是整数，转换为字符串并添加

        # 处理 "frame_pts" 字段
        if "frame_pts" in item:
            frame_pts_value = item["frame_pts"]
            if isinstance(frame_pts_value, str):
                frame_pts_values += frame_pts_value.split(":")[-1].split("/")  # 拆分并添加到 frame_pts_values
            elif isinstance(frame_pts_value, int):
                frame_pts_values.append(str(frame_pts_value))  # 如果是整数，转换为字符串并添加

        # ---------------------------------------------MV处理代码------------------------------------------------#
        if "MV" in item:
            mv_split_values = item["MV"].split(":")[-1].split("/")  # 拆分 MV 字段
            # 只添加第二和第三个值
            if len(mv_split_values) >= 3:
                mv_values.append("MV[0]")
                mv_values.append(mv_split_values[0])  # 第一个值   veh_spd（车速）
                mv_values.append("MV[1]")
                mv_values.append(mv_split_values[1])  # 第二个值
                mv_values.append("MV[2]")
                mv_values.append(mv_split_values[4])  # 第五个值
                mv_values.append("MV[3]")
                mv_values.append(mv_split_values[5])  # 第六个值
                mv_values.append("MV[4]")
                mv_values.append(mv_split_values[6])  # 第七个值

        # 处理 "Ba" 字段
        if "Ba" in item:
            mv_split_values = item["Ba"].split(":")[-1].split("/")  # 拆分 Ba 字段
            if len(mv_split_values) >= 3:
                mv_values.append("MV[5]")
                mv_values.append(mv_split_values[0])  # 第1个值
                mv_values.append("MV[6]")

                mv_values.append(mv_split_values[1])  # 第2个值

        # 处理 "Ac" 字段
        if "Ac" in item:
            mv_split_values = item["Ac"].split(":")[-1].split("/")  # 拆分 Ac 字段
            if len(mv_split_values) >= 3:
                mv_values.append("MV[7]")

                mv_values.append(mv_split_values[0])  # 第1个值
                mv_values.append("MV[8]")

                mv_values.append(mv_split_values[1])  # 第2个值

        # 处理 "vp" 字段
        if "vp" in item:
            mv_split_values = item["vp"].split(":")[-1].split("/")  # 拆分 vp 字段
            if len(mv_split_values) >= 3:
                mv_values.append("MV[9]")

                mv_values.append(mv_split_values[1])  # 第二个值

        # 处理 "mv3" 字段
        if "mv3" in item:
            mv_split_values = item["mv3"].split(":")[-1].split("/")  # 拆分 mv3 字段
            if len(mv_split_values) >= 3:
                mv_values.append("MV[10]")
                mv_values.append(mv_split_values[0])  # 第1个值
                mv_values.append("MV[11]")
                mv_values.append(mv_split_values[1])  # 第2个值
                mv_values.append("MV[12]")
                mv_values.append(mv_split_values[2])  # 第3个值
                mv_values.append("MV[13]")
                mv_values.append(1)                   # veh_spd_unit
                mv_values.append("MV[14]")
                mv_values.append(2)                   # veh_total_mileage

        # ---------------------------------------------MV处理代码结束------------------------------------------------#

        # 直接从现成的键值对获取 outer_value 和 value
        for outer_value, t_value in item.items():
            if outer_value == "H" and t_value.endswith("m"):
                t_value = t_value.replace("m", "")  # 去掉 "m"
            if outer_value == "Pt" and '/' in t_value:
                t_value = t_value.split('/')[0]  # 只保留第一个值
            if outer_value in outer_fields:
                if current_outer[outer_value] != t_value or current_outer[outer_value] is None:
                    if all(current_outer[field] is not None for field in outer_fields) or frame_dict['id'] == ['0']:
                        # 将当前组添加到输出
                        output.append({
                            **current_outer,
                            "SEN": 0,
                            "VP":175,
                            "frames": current_object
                        })
                    # 更新当前外层字段
                    current_outer[outer_value] = t_value
                    current_object = []

        # 当 frame_id、frame_pts 和 MV 都有值时，将它们合并
        # if frame_id_values == ['-1']:
        #     current_object.append(frame_id_values)
        #     frame_id_values = []
        #     frame_pts_values = []
        #     mv_values = []

#---------------------------------------

        # 假设需要的元素数量是 15  or  30
        required_length = 15

        if frame_id_values and frame_pts_values and mv_values and len(mv_values) == required_length:
            frame_dict = {
                "id": frame_id_values,
                "JT": frame_pts_values,
                "MV": mv_values
            }

            # 合并字典中的键值对，并添加到 current_object
            current_object.append(frame_dict)

            # 重置 frame_id、frame_pts 和 MV 的状态，为下一次数据准备
            frame_id_values = []
            frame_pts_values = []
            mv_values = []

    # 将最后一组数据添加到输出
    if all(current_outer[field] is not None for field in outer_fields):
        output.append({
            **current_outer,
            "SEN": 0,
            "VP": 175,
            "frames": current_object
        })

    # 后处理：将所有数字字符串转换为浮动类型，frame_id 转换为整数类型
    for entry in output:
        # pdb.set_trace()
        for outer_field in outer_fields:
            # 如果是数字字符串，则转换为浮动类型
            if entry[outer_field]:
                try:
                    entry[outer_field] = float(entry[outer_field])  # 尝试转换为浮动类型
                except ValueError:
                    pass  # 如果转换失败，保持原值（不做更改）

        # 对 frames 内的每个条目进行后处理
        for frame in entry.get("frames", []):
            for key in ["id", "JT", "MV"]:
                if key in frame:
                    if key == "id":
                        # 处理 id 字段，将其转换为整数类型并转换为非数组
                        if isinstance(frame[key], list):
                            frame[key] = int(frame[key][0]) if frame[key] else None
                    elif key == "JT":
                        # 处理 JT 字段，将其转换为整数类型并转换为非数组
                        if isinstance(frame[key], list):
                            frame[key] = int(frame[key][0]) if frame[key] else None
                    else:
                        # 处理 MV 和其他列表中的值，确保它们是浮动类型
                        if isinstance(frame[key], list):
                            frame[key] = [
                                float(val) if isinstance(val, str) and val.replace('.', '', 1).isdigit() else val
                                for val in frame[key]
                            ]

                    # 如果 frame[key] 是可迭代对象（如列表），则进行转换
                    if isinstance(frame[key], list):
                        for i, val in enumerate(frame[key]):
                            try:
                                if isinstance(val, str):  # 只有字符串才进行处理
                                    if key == "id":
                                        frame[key][i] = int(val)  # 对 frame_id 转换为整数
                                    elif key == "JT":
                                        frame[key][i] = int(val)  # 对 JT 转换为整数
                                    else:
                                        frame[key][i] = float(val)  # 对其他字段转换为浮动类型
                            except ValueError:
                                pass
                    # 如果不是列表（如整数），直接转换
                    elif isinstance(frame[key], str):
                        try:
                            if key == "id":
                                frame[key] = int(frame[key])
                            elif key == "JT":
                                frame[key] = int(frame[key])
                            else:
                                frame[key] = float(frame[key])
                        except ValueError:
                            pass

    return {
        "video_name": video_name,
        "json_name": json_name,
        "parameters": output  # 包含所有参数
    }


# 读取输入文件并处理数据
def process_file(input_path, output_path, outer_fields=None, inner_fields=None):
    # 通过 script1 读取 JSON 数据
    extracted_data = parse_json_and_extract_info(input_path)

    # 处理数据
    processed_data = process_data(extracted_data, outer_fields,input_file=input_path)

    # 将处理后的数据写入输出文件
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(processed_data, outfile, ensure_ascii=False, indent=4)


# 示例路径
input_path = r"C:\Users\1\Downloads\H264_parse_tool-develop_wgma-9a44b704f88ac00c15ee1f800031df6d574d8ab1\H264_parse_tool-develop_wgma\0000000000000000-241123-144903-144948-000001001050.json"  # 输入文件路径
output_path = r"C:\Users\1\Desktop\18通道提取\test17.json"  # 输出文件路径

# 示例：调用文件处理函数
outer_fields = ["H", "CW", "LM", "HL", "Pt"]  # 选择 LM 和 HL 作为外层字段


# 调用函数进行处理
process_file(input_path, output_path, outer_fields)



