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
    subprocess.run(['python', 'check.py'])
    print("Scrapping completed")
    with open('output.json', 'r') as file:
        data = json.load(file)
    url = 'https://skitter-adaptable-shallot.glitch.me/receive-data'  # Replace with your Node.js server URL
    files = {'file': ('output.json', json.dumps(data), 'application/json')}
    response = requests.post(url, files=files)
    print(response.json())
    # Read the output.json file
    

# Create a scheduler
scheduler = BackgroundScheduler()
# scheduler.add_job(run_check, 'interval', minutes=5)  # Set the interval (e.g., every 5 minutes)
scheduler.add_job(run_check,'cron',minute='*/5',replace_existing=True, misfire_grace_time=3600)
# run_check()
# Flask route for triggering the task manually
# try:
#     os.system('./script.sh')
#     print("script running successfully")
# except:
#     print("error running script")
result = subprocess.run(['./script.sh'], capture_output=True, text=True)
chromium_path = result.stdout.strip()
print(result.stderr)

# Add the Chromium path to the PATH environment variable
os.environ['PATHCHROME'] =  chromium_path
os.environ["PATH"]+=":"+chromium_path

# Verify the updated PATH
print(os.environ['PATH'])
time.sleep(4)
run_check()
scheduler.start()
# run_check()
@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    # Start the scheduler

    # Run the Flask app
    app.run()
