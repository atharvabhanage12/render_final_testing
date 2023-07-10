import asyncio
from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
import os
import time

folder_path = './passed'  # Replace with the actual folder path

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

app = Flask(__name__)
executor = ThreadPoolExecutor()
result_dict = {
    'company_name_list': [],
    'company_posting_array': [],
    "error-companies": []
}

L = []
for i in file_list:
    if i.endswith(".py"):
        new_file = os.path.join(folder_path, i)
        L.append(new_file)

count = 0

async def run_check():
    global result_dict
    global count
    print("running process " + L[count])
    result = subprocess.run(['python', L[count]], capture_output=True, text=True)
    result_dict["error-companies"].append({"name": L[count], "error": result.stderr, "output": result.stdout})
    output_json = json.loads(result.stdout)
    company_name = output_json['company']
    jobs_data = output_json['data']
    result_dict['company_name_list'].append(company_name)
    result_dict['company_posting_array'].append(jobs_data)
    with open('output1.json', 'w') as file:
        json.dump(result_dict, file, indent=4)
    print("execution completed")

    count += 1
    count = count % len(L)
    if count == 0:
        result_dict = {
            'company_name_list': [],
            'company_posting_array': [],
            "error-companies": []
        }
        with open('output.json', 'w') as file:
            json.dump(result_dict, file, indent=4)

def install_chrome():
    result = subprocess.run(['python', 'temp.py'])
    # print(result.stdout)
install_chrome()

@app.route('/cronjob', methods=['GET'])
def run_task():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_check())  # Await the execution of run_check function
    return {"message": "Pinged server successfully"}

@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as a JSON response
    return jsonify(data)

@app.route('/receive-test-data', methods=['GET'])
def send_dataone():
    # with open('output1.json', 'r') as file:
    #     data = json.load(file)
    
    # # Return the data as a JSON response
    # return jsonify(data)
    return jsonify(result_dict)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
