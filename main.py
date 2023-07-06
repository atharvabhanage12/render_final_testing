import time
import os
import requests
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import json
import subprocess
import signal
import sys

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
    scheduler.remove_all_jobs()  # Terminate the previous job
    # time.sleep(300)  # Sleep for 5 minutes (300 seconds)
    start_new_cron_job()  # Start a new cron job instance

# Start a new cron job instance
def start_new_cron_job():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_check, 'cron', minute='*/5', replace_existing=True)
    scheduler.start()

# Catch the SIGTERM signal
def handle_sigterm(signal, frame):
    # Perform any necessary cleanup or shutdown procedures here
    # For example, stop the scheduler and release any resources
    
    # Stop the scheduler
    try:
        scheduler.shutdown()
    except:
        print("sigterm error")
    scheduler.remove_all_jobs()
    print("sigterm")
    start_new_cron_job()

    # Exit the application
    # sys.exit(0)

# Register the SIGTERM signal handler
signal.signal(signal.SIGTERM, handle_sigterm)

# Create a scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(run_check, 'cron', minute='*/5', replace_existing=True)
result = subprocess.run(['./script.sh'], capture_output=True, text=True)
chromium_path = result.stdout.strip()
print(result.stderr)

# Add the Chromium path to the PATH environment variable
os.environ['PATHCHROME'] =  chromium_path
os.environ["PATH"]+=":"+chromium_path

# Verify the updated PATH
print(os.environ['PATH'])

# Start the scheduler
scheduler.start()

@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask app
    app.run()
