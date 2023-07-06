import random
import subprocess
import os
import json

folder_path = './passed'  # Replace with the actual folder path

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

result_dict = {
    'company_name_list': [],
    'company_posting_array': []
}

random_file = None

while random_file is None or not random_file.endswith('.py'):
    random_file = random.choice(file_list)

file_path = os.path.join(folder_path, random_file)
print(f"Running file: {random_file}")

try:
    # Run the Python file using subprocess
    result = subprocess.run(['python', file_path], capture_output=True, text=True)
    print(result.stderr)
    
    # Convert the output to JSON
    output_json = json.loads(result.stdout)

    # Extract the company name and data from the output
    company_name = output_json['company']
    jobs_data = output_json['data']

    # Add the company name to companies_list
    result_dict['company_name_list'].append(company_name)

    # Add the jobs data to jobs_list
    result_dict['company_posting_array'].append(jobs_data)

    # Print the output of the file
    print(result_dict["company_name_list"])

except subprocess.CalledProcessError as e:
    # Print the error message and the filename for which the error occurred
    print(f"Error running file: {random_file}")
    print(e.stderr)

print("==============================================")

# Write the final dictionary to output.json
with open('output.json', 'w') as file:
    json.dump(result_dict, file, indent=4)
