"""
CSV to JSONL Converter for OpenAI Fine-Tuning

Usage:
- Place your input CSV file at: input/input.csv
- The CSV must contain the following columns with headers:
    status,status_type,substatus_type

    Example row:
    shipment has been cancelled,Exception,Cancelled

- The script will generate a JSONL file at: output/output.jsonl
- This JSONL format is compatible with OpenAI's fine-tuning API.

Notes:
- If substatus_type is empty or 'null', it will be set to null in JSON.
- A system prompt is included in each message based on predefined status type/substatus type pairs.
- Progress will be printed to the terminal as each row is processed.
"""

import csv
import json

STATUS_CATEGORIES_DICT = {
    "Exception": [
        "Cancelled",
        "Carrier Delays",
        "Claims Issued",
        "Customs/Tax Delays",
        "Delayed",
        "Incorrect Info",
        "Loss/Returns",
        "Natural Causes",
        "Other Delays",
        "Returned",
        "Traffic Delays",
    ],
    "Info": [None],
    "Transit": [
        None,
        "Customs/Tax Delays",
        "Delayed",
        "Delivered",
        "Documents Handover",
        "Incorrect Info",
        "Onboard at Departure Terminal",
        "Other Delays",
        "Pick Up Confirmed",
    ],
}

# Convert dictionary to list of (status_type, substatus_type) pairs
status_pairs = [(k, v) for k, values in STATUS_CATEGORIES_DICT.items() for v in values]

# Create system prompt
system_prompt = (
    f"Classify the given status into a status type and substatus type using only these valid pairs: {status_pairs}"
)

# File paths
csv_file_path = "input/input.csv"
jsonl_file_path = "output/output.jsonl"

required_fields = {"status", "status_type", "substatus_type"}

# Read CSV and write JSONL
with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile, \
     open(jsonl_file_path, 'w', encoding='utf-8') as jsonlfile:

    reader = list(csv.DictReader(csvfile))
    total = len(reader)

    if not reader or not required_fields.issubset(reader[0].keys()):
        raise ValueError(f"Missing required columns. Found: {reader[0].keys()}")

    for i, row in enumerate(reader, start=1):
        status = row.get("status")
        status_type = row.get("status_type")
        substatus_type = row.get("substatus_type")

        # Convert "null", "None", empty string to actual None
        substatus_type = None if substatus_type in ("null", "None", "") else substatus_type

        json_line = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Classify the status: `{status}`"},
                {"role": "assistant", "content": json.dumps({
                    "status": status,
                    "status_type": status_type,
                    "substatus_type": substatus_type
                })}
            ]
        }

        jsonlfile.write(json.dumps(json_line) + '\n')
        print(f"Processed {i}/{total}", end="\r")

print(f"\nFinished writing {total} records to {jsonl_file_path}.")
