
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

async def run_check():
    global result_dict

    for count, script_path in enumerate(L):
        logger.info(f"Running script {count + 1}/{len(L)}: {script_path}")
        
        try:
            process = await asyncio.create_subprocess_exec(
                'python', script_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            logger.info(f"Script output from {script_path}: {stdout.decode()}")
            logger.info(f"Script errors from {script_path}: {stderr.decode()}")

            # if stderr:
            #     result_dict["error-companies"].append({"name": script_path, "error": stderr.decode(), "output": stdout.decode()})

            try:
                with open('output1.json', 'r') as file:
                    output_json = json.load(file)
                    company_name = output_json['company']
                    jobs_data = output_json['data']
                    if((count!=0) and (company_name ==result_dict['company_name_list'][-1])):
                         result_dict["error-companies"].append({"name": script_path, "error": stderr.decode(), "output": stdout.decode()})

                    else:
                        result_dict['company_name_list'].append(company_name)
                        result_dict['company_posting_array'].append(jobs_data)
                        logger.info(f"Data collected for {company_name}")
            except json.JSONDecodeError:
                logger.error(f"Error parsing JSON from output1.json for {script_path}")
        
        except Exception as e:
            logger.error(f"Exception running script {script_path}: {e}")

    with open('output.json', 'w') as file:

        json.dump(result_dict, file, indent=4)
    logger.info("Execution of all scripts completed")

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
