import json
import math
import pandas as pd
from datetime import datetime
import os
import argparse
# Function to extract the data from JSON
def parse_json_and_extract_info(jsonFile):
    with open(jsonFile, 'r') as json_file:
        parsed_json = json.load(json_file)

    # Initialize data structures
    extracted_data = []
    processed_frame_ids = set()

    # Loop through video frames
    for videoIndex in range(len(parsed_json["ai_info"])):
        ai_info = parsed_json["ai_info"]
        frames = ai_info.get("frames", [])

        for frame in frames:
            frame_id = frame.get("frame_id")
            if frame_id >= 0:
                frame_time = frame.get("rtc_time", "unknown time")

                # Skip already processed frames
                if frame_id in processed_frame_ids:
                    continue

                # Initialize a dictionary for the current frame
                frame_data = {
                    "frame_id": frame_id,
                    "rtc_time": frame_time,
                    "CYaw": None,  # Default value if CYaw is not found
                    "Pt": None    # Default value if Pt is not found
                }

                # Process frame info for CYaw and Pt
                for info in frame.get("infos", []):
                    for text in info.get("text", []):
                        t_value = str(text.get("t", ""))
                        if t_value.startswith("CYaw:"):
                            frame_data["CYaw"] = t_value.split(":")[1]
                        elif t_value.startswith("Pt:"):
                            frame_data["Pt"] = t_value.split(":")[1].split('/')[0]  # Extract first value before slash

                # Append the grouped dictionary to extracted_data
                extracted_data.append(frame_data)
                processed_frame_ids.add(frame_id)

    return extracted_data


from datetime import datetime

def detect_changes(extracted_data, folder_name, field_name):
    """
    Detect changes in the specified field (CYaw or Pt) and record the changes.

    Args:
        extracted_data (list): List of dictionaries with grouped frame data.
        folder_name (str): Name of the folder (video segment).
        field_name (str): The key to detect changes for (e.g., 'CYaw', 'Pt').

    Returns:
        list: A list of records showing the start, changes, and end values.
    """
    change_records = []  # To store the change records
    last_value = None  # To track the last value of the field
    last_time = None  # To track the last valid time
    first_record = None  # To store the first record

    for frame in extracted_data:
        value = frame.get(field_name)
        frame_time = frame.get("rtc_time", "unknown time")

        # Skip invalid time entries
        if value is None or frame_time == "unknown time":
            continue

        try:
            # Convert time string to datetime object for comparison
            current_time = datetime.strptime(frame_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue  # Skip invalid time formats

        # Start record: Set the initial value
        if last_value is None:
            last_value = value
            last_time = current_time
            first_record = {
                "name": folder_name,
                "time": frame_time,
                field_name: value,
                f"{field_name}_弧度值": float(value) * (180 / math.pi),
                "time_diff": "开始",
                "中断": 1
            }
            change_records.append(first_record)
        else:
            # Calculate the time difference in seconds
            time_diff = (current_time - last_time).total_seconds()

            # Detect change in value
            if float(value) != float(last_value):
                change_records.append({
                    "name": folder_name,
                    "time": frame_time,
                    field_name: value,
                    f"{field_name}_弧度值": float(value) * (180 / math.pi),
                    "time_diff": time_diff,  # Time difference in seconds
                    "中断": 0
                })
                last_value = value  # Update the last value
                last_time = current_time  # Update the last time

    # Add a final "结束" record without time difference calculation
    if first_record:
        change_records.append({
            "name": folder_name,
            "time": frame_time,  # Use the last valid time
            field_name: last_value,
            f"{field_name}_弧度值": float(last_value) * (180 / math.pi),
            "time_diff": "结束",  # Force "结束"
            "中断": 1
        })

    return change_records


# Function to write data to Excel
def write_to_excel(cyaw_records, pt_records, output_file):
    with pd.ExcelWriter(output_file) as writer:
        pd.DataFrame(cyaw_records).to_excel(writer, index=False, sheet_name="CYaw Changes")
        pd.DataFrame(pt_records).to_excel(writer, index=False, sheet_name="Pt Changes")

# Function to recursively search for JSON files and process them
def process_json_recursively(root_directory):
    for dirpath, _, filenames in os.walk(root_directory):
        for file in filenames:
            if file.endswith(".json"):
                json_path = os.path.join(dirpath, file)

                # Extract the folder name and output Excel file path
                folder_name = os.path.splitext(file)[0]
                output_file = os.path.join(dirpath, f"{folder_name}.xlsx")

                # Extract data and detect changes
                extracted_data = parse_json_and_extract_info(json_path)
                cyaw_records = detect_changes(extracted_data, folder_name, "CYaw")
                pt_records = detect_changes(extracted_data, folder_name, "Pt")

                # Write to Excel
                write_to_excel(cyaw_records, pt_records, output_file)
                print(f"Processed '{json_path}' -> '{output_file}'")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process JSON files to extract CYaw and Pt changes.")
    parser.add_argument('-i', '--input_directory', required=True, type=str, help="Input directory containing JSON files.")
    parser.add_argument('-o', '--output_directory', required=True, type=str, help="Output directory for saving Excel files.")
    args = parser.parse_args()

    # Process the JSON files and generate the Excel files
    process_json_recursively(args.input_directory)

if __name__ == "__main__":
    main()