import subprocess
import os
import json
import concurrent.futures

folder_path = './passed'  # Replace with the actual folder path

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

result_dict = {
    'company_name_list': [],
    'company_posting_array': []
}
count=0
def run_python_file(file_name):
    global count
    count+=1
    if file_name.endswith('.py'):  # Check if the file is a Python file
        file_path = os.path.join(folder_path, file_name)
        print(f"Running file: {file_name}")

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
            # print(result.stdout)
            print(result_dict["company_name_list"])
            # print(result_dict)

        except subprocess.CalledProcessError as e:
            # Print the error message and the filename for which the error occurred
            print(f"Error running file: {file_name}")
            print(e.stderr)

        print("==============================================")

# Use a ThreadPoolExecutor to run multiple files concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    executor.map(run_python_file, file_list)
print(result_dict["company_name_list"])
# Write the final dictionary to output.json
with open('output.json', 'w') as file:
    json.dump(result_dict, file, indent=4)