import time

import os
import requests
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import json
import subprocess

app = Flask(__name__)

# Define the task to run at intervals
def run_check():
    # Execute check.py using subprocess
    print("running process...")
    # subprocess.run(['python', 'check.py'])
    
    # Read the output.json file

    # Send a POST request to the desired URL
    print("Scrapping Successful")

# Create a scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(run_check, 'interval', minutes=0.1)
result = subprocess.run(['./script.sh'], capture_output=True, text=True)
chromium_path = result.stdout.strip()
print(result.stderr)

# Add the Chromium path to the PATH environment variable
os.environ['PATHCHROME'] =  chromium_path
os.environ["PATH"]+=":"+chromium_path

# Verify the updated PATH
print(os.environ['PATH'])

# run_check()
# scheduler.start()
# run_check()
@app.route('/',methods=['GET'])
def start_server():
    print("starting server")
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_check, 'interval', minutes=0.1)
    scheduler.start()
    return {"message":"server started succesfully"}
@app.route('/receive-data', methods=['GET'])
def send_data():
    # Read the output.json file
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    # run_check()
    app.run()
