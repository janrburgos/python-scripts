"""
JSON to CSV Converter for OpenAI Carrier Status Classification Results

Usage:
- Place one or more JSON response files inside the `input/` folder.
- Each JSON file must have a top-level key: `classified_statuses` (list of dicts).
- This script will extract all classified statuses and output a CSV file at:
  `output/classified_statuses.csv`

The resulting CSV will have columns:
- status_name
- status_type
- substatus_type

Progress will be printed to the terminal as each row is processed.
"""

import os
import json

input_folder = "input"
output_file = "output/classified_statuses.csv"

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Collect all .json files in input folder
json_files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

# Prepare rows to write to CSV
all_statuses = []

total_files = len(json_files)

for i, file_name in enumerate(json_files, start=1):
    file_path = os.path.join(input_folder, file_name)

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
        statuses = data.get("classified_statuses", [])
        for status in statuses:
            status_name = status.get("status_name", "")
            status_type = status.get("status_type", "")
            substatus_type = status.get("substatus_type", None)
            all_statuses.append((status_name, status_type, substatus_type))

    print(f"Processed {i}/{total_files}", end="\r")

# Write to CSV
with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
    csvfile.write("status_name,status_type,substatus_type\n")
    for status_name, status_type, substatus_type in all_statuses:
        substatus_value = "" if substatus_type is None else substatus_type
        line = f'"{status_name}","{status_type}","{substatus_value}"\n'
        csvfile.write(line)

print(f"\nFinished writing {len(all_statuses)} rows to {output_file}.")
