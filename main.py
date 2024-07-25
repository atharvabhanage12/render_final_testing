import asyncio
from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

L = [os.path.join(folder_path, i) for i in file_list if i.endswith(".py")]

count = 0

async def run_check():
    global result_dict
    global count

    script_path = L[count]
    logger.info(f"Running process: {script_path}")
    
    try:
        # Use asyncio's subprocess for better async handling
        process = await asyncio.create_subprocess_exec(
            'python', script_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        
        logger.debug(f"Script output: {stdout.decode()}")
        logger.debug(f"Script errors: {stderr.decode()}")

        result_dict["error-companies"].append({"name": script_path, "error": stderr.decode(), "output": stdout.decode()})

        with open('output1.json', 'r') as file:
            output_json = json.load(file)
            company_name = output_json['company']
            jobs_data = output_json['data']
            result_dict['company_name_list'].append(company_name)
            result_dict['company_posting_array'].append(jobs_data)

    except json.JSONDecodeError:
        logger.error(f"Error parsing JSON from output1.json")
    except Exception as e:
        logger.error(f"Exception running script {script_path}: {e}")

    with open('output.json', 'w') as file:
        json.dump(result_dict, file, indent=4)
    logger.info("Execution completed")

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
    logger.debug(f"Chrome installation output: {result.stdout}")

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
    with open('output1.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as a JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
