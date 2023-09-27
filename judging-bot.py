import sys
import os
import shutil

def organize_by_severity(repository_path):
    # Ensure the severity directories exist
    for severity in ["High", "Medium", "Invalid"]:
        severity_dir = os.path.join(repository_path, severity)
        if not os.path.exists(severity_dir):
            # cd mkdir - this line makes a directory
            os.makedirs(severity_dir)

    # Iterate through all files in the repository
    for file_name in os.listdir(repository_path):
        # if markdown file then parse
        if file_name.endswith(".md"):
            file_path = os.path.join(repository_path, file_name)
            parsed_details = parse_markdown_v2(file_path)
            severity = parsed_details["Severity"].strip()

            print(f"Parsed Severity for {file_name}: {severity}")
            
            # Ensure the severity is one of the recognized ones
            if severity in ["High", "Medium", "Invalid"]:
                # Move the file to the appropriate directory
                new_path = os.path.join(repository_path, severity, file_name)
                print(f"Moving {file_path} to {new_path}")
                shutil.move(file_path, new_path)
            else:
                print(f"Unrecognized Severity in file {file_name}: {severity}")

def parse_markdown_v2(file_path):
    # Dictionary to store the extracted details
    details = {
        "Auditor": "",
        "Severity": "",
        "Summary": "",
        "Vulnerability Detail": "",
        "Impact": "",
        "Code Snippet": "",
        "Tool used": "",
        "Recommendation": ""
    }
    
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.readlines()
    
    # Set the Auditor name and Severity from the first & third lines
    details["Auditor"] = content[0].strip()
    details["Severity"] = content[2].strip().capitalize()
    
    # Temporary variables to store multi-line data
    current_section = None
    current_data = []
    
    # Iterate through each line in the content
    for line in content[3:]:  # Skip the first two lines
        # Check if the line indicates the start of a new section
        if line.startswith("## "):
            # If we were already in a section, save the accumulated data to the details dictionary
            if current_section:
                details[current_section] = "\n".join(current_data).strip()
                current_data = []
            
            # Set the current section to the new section (after removing "## " and trimming)
            current_section = line.replace("## ", "").strip()
        else:
            # Otherwise, accumulate data for the current section
            current_data.append(line.strip())
    
    # Handle the last section data
    if current_section:
        details[current_section] = "\n".join(current_data).strip()
    
    return details

# Test the updated function with the provided markdown content
# parsed_details_v2 = parse_markdown_v2(file_path)
# parsed_details_v2

# Run in terminal for parse markdown
if __name__ == "__main__":
    action = sys.argv[1]

    if action == "parse":
        file_path = sys.argv[2]
        parsed_details = parse_markdown_v2(file_path)
        for key, value in parsed_details.items():
            print(f"{key}: {value}\n")
    elif action == "organize":
        repository_path = sys.argv[2]
        organize_by_severity(repository_path)
    else:
        print("Unknown action. Use 'parse' for parsing a single file or 'organize' for organizing a directory.")
