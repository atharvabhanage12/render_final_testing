from datetime import datetime, timedelta
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from flask import Flask, jsonify
import os, json
import subprocess

app = Flask(__name__)

scheduler = AsyncIOScheduler()

def long_running_task():
    # Your long-running task logic here
    print("Running long-running task...")
    result = subprocess.run(['python', 'check.py'], capture_output=True, text=True)
    print("Task completed successfully")

def schedule_job():
    scheduler.add_job(long_running_task, 'interval', minutes=0.1)
    scheduler.start()

@app.route('/')
def home():
    return "Flask Server with Cron Job Example"

# result = subprocess.run(['./script.sh'], capture_output=True, text=True)
# chromium_path = result.stdout.strip()
# print(result.stderr)

# # Add the Chromium path to the PATH environment variable
# os.environ['PATHCHROME'] =  chromium_path
# os.environ["PATH"]+=":"+chromium_path

# # Verify the updated PATH
# print(os.environ['PATH'])

@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    schedule_job()
    app.run()
