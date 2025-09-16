import json
import os

# Create or load your data as a Python dictionary
data = {
    "CostPerKwh": 0.39,
    "MaxGridCurrent": 16,
}

# Get the directory of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))
print("Directory of the current Python script:", script_directory)

file_path = os.path.join(script_directory, "DCWB_Config.json")

# Serialize the data to a JSON-formatted string
json_string = json.dumps(data, indent=4)  # The `indent` argument adds formatting for readability

# Open or create the JSON file for writing
with open(file_path, "w") as json_file:
    # Write the JSON data to the file
    json_file.write(json_string)

# Close the file
