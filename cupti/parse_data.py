import csv
import re

# Input and output file paths
input_file = "./pc_sampling_utility/log.txt"
output_file = "./performance_counters.csv"

# Regular expression to match function entries
entry_pattern = re.compile(r'functionName: (?P<functionName>\S+), .*? pcOffset: (?P<pcOffset>\d+), (.*)')

# Dictionary to store extracted data
data = []

# Read and process the file
with open(input_file, "r") as file:
    for line in file:
        match = entry_pattern.search(line)
        if match:
            entry = match.groupdict()
            extra_data = match.group(3)
            
            # Extract performance counters, keeping only the suffix
            counters = {key.split("smsp__pcsamp_warps_issue_stalled_")[-1]: value for key, value in 
                        (item.split(": ") for item in extra_data.split(", ") if "smsp__pcsamp_warps_issue_stalled_" in item)}
            
            # Merge function name, pcOffset, and performance counters
            entry.update(counters)
            data.append(entry)

# Get all unique counter keys
all_counters = sorted(set(key for row in data for key in row.keys() if key not in ["functionName", "pcOffset"]))

# Write to CSV
with open(output_file, "w", newline="") as csvfile:
    fieldnames = ["functionName", "pcOffset"] + all_counters
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"CSV file '{output_file}' has been created successfully.")


