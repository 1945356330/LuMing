#!/bin/bash

# Get the current script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Define script paths
SCRIPT1="$SCRIPT_DIR/1.py"
SCRIPT2="$SCRIPT_DIR/2.py"

# Parse command-line arguments
while getopts "i:o:" opt; do
    case $opt in
        i) INPUT_DIR="$OPTARG" ;;
        o) OUTPUT_DIR="$OPTARG" ;;
        *) echo "Usage: $0 -i <input_dir> -o <output_dir>"; exit 1 ;;
    esac
done

# Check if both input and output directories are provided
if [[ -z "$INPUT_DIR" || -z "$OUTPUT_DIR" ]]; then
    echo "Both input and output directories must be specified."
    echo "Usage: $0 -i <input_dir> -o <output_dir>"
    exit 1
fi

# Run the first Python script (script1.py)
echo "Running script1.py (Processing JSON files)..."
python3 "$SCRIPT1" -i "$INPUT_DIR" -o "$OUTPUT_DIR"

# Run the second Python script (script2.py)
echo "Running script2.py (Merging Excel files)..."
python3 "$SCRIPT2" -i "$INPUT_DIR" -o "$OUTPUT_DIR"

echo "Both scripts executed successfully."
