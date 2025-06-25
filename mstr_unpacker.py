import zipfile
import os
import html
import json
import re


# Define the path and extraction directory
mstr_zip_path = "mstr_files/Call Center Insights.mstr"
extracted_dir = "mstr_files/call_center_insights_extracted"

# Extract the ZIP contents
with zipfile.ZipFile(mstr_zip_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir)

# List all extracted files
extracted_files = []
for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        extracted_files.append(os.path.join(root, file))

# Function to extract readable ASCII strings from a file
def extract_strings_from_file(file_path, min_length=3):
    with open(file_path, 'rb') as f:
        data = f.read()
    result = []
    current = b""
    for byte in data:
        if 32 <= byte <= 126 or byte in (9, 10, 13):  # ASCII printable + whitespace
            current += bytes([byte])
        else:
            if len(current) >= min_length:
                result.append(current.decode('ascii', errors='replace'))
            current = b""
    if len(current) >= min_length:
        result.append(current.decode('ascii', errors='replace'))
    return result

# Extract strings from all extracted files
all_extracted_strings = {}
for file_path in extracted_files:
    try:
        strings = extract_strings_from_file(file_path)
        all_extracted_strings[file_path] = strings
    except Exception as e:
        all_extracted_strings[file_path] = [f"Error reading file: {str(e)}"]
