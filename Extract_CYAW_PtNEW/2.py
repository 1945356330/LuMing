import os
import re
import pandas as pd
import argparse
def extract_time_keyword(filename):
    """
    Extract the time keyword from the file name and convert it to a sortable format.
    Example: 075435-085435 -> 07:54:35 (start time only)
    """
    match = re.search(r'(\d{6})-(\d{6})', filename)
    if match:
        start_time = match.group(1)  # Extract 075435
        return f"{start_time[:2]}:{start_time[2:4]}:{start_time[4:]}"  # Format to 07:54:35
    return "99:99:99"  # Default high value if no match is found (push invalid to end)

def find_excel_files(root_directory):
    """
    Recursively find all Excel files in the root directory and its subdirectories.
    """
    excel_files = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".xlsx") and not file.startswith("~$"):  # Exclude temporary Excel files
                full_path = os.path.join(root, file)
                excel_files.append(full_path)
    return excel_files

def merge_excel_files(input_directory, output_file):
    """
    Merge all Excel files in the input directory and its subdirectories into a single Excel file.
    - CYaw Changes
    - Pt Changes
    Rows are sorted based on the extracted time keyword from the file names.
    """
    pt_data = []      # To store data for Pt Changes
    cyaw_data = []    # To store data for CYaw Changes

    # Find all Excel files
    excel_files = find_excel_files(input_directory)

    # Sort the files based on the extracted time keyword
    excel_files.sort(key=lambda x: extract_time_keyword(os.path.basename(x)))

    # Process each Excel file
    for file_path in excel_files:
        file_name = os.path.basename(file_path)
        try:
            # Read Pt and CYaw sheets
            pt_df = pd.read_excel(file_path, sheet_name="Pt Changes")
            cyaw_df = pd.read_excel(file_path, sheet_name="CYaw Changes")

            # Add a column to indicate the source file name
            # pt_df['Source_File'] = file_name
            # cyaw_df['Source_File'] = file_name

            # Append data to the lists
            pt_data.append(pt_df)
            cyaw_data.append(cyaw_df)

        except Exception as e:
            print(f"Error reading {file_name}: {e}")

    # Combine all Pt Changes and CYaw Changes into single dataframes
    combined_pt = pd.concat(pt_data, ignore_index=True) if pt_data else pd.DataFrame()
    combined_cyaw = pd.concat(cyaw_data, ignore_index=True) if cyaw_data else pd.DataFrame()

    # Write the combined data to a single Excel file with two sheets
    with pd.ExcelWriter(output_file) as writer:
        if not combined_cyaw.empty:
            combined_cyaw.to_excel(writer, index=False, sheet_name="CYaw Changes")
        if not combined_pt.empty:
            combined_pt.to_excel(writer, index=False, sheet_name="Pt Changes")

    print(f"All Excel files have been merged and saved to {output_file}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Merge Excel files into a single file sorted by time.")
    parser.add_argument('-i', '--input_directory', required=True, type=str, help="Root directory containing Excel files.")
    parser.add_argument('-o', '--output_directory', required=True, type=str, help="Directory to save the merged Excel file.")
    args = parser.parse_args()

    # Get the output file name from the directory structure
    base_name = os.path.basename(args.input_directory)
    

    path_parts = args.input_directory.split(os.sep)
    folder_name = path_parts[-2]  # "ADplus_LK_LC"
    date = path_parts[-1]         # "2024-11-18"
    
    # Combine folder name and date to form the output file name
    output_filename = f"{folder_name}-{date}.xlsx"
    output_file = os.path.join(args.output_directory, output_filename)


    # output_file = os.path.join(args.output_directory, f"{base_name}.xlsx")

    # Ensure the output directory exists
    os.makedirs(args.output_directory, exist_ok=True)

    # Merge Excel files
    merge_excel_files(args.input_directory, output_file)

if __name__ == "__main__":
    main()