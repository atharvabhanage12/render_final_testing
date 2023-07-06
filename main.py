import time
import os
import requests
from flask import Flask, jsonify
import json
import subprocess
import schedule

import threading

app = Flask(__name__)

# Define the task to run at intervals
def run_check():
    # Execute check.py using subprocess
    print("running process...")
    subprocess.run(['python', 'check.py'])
    
    # Read the output.json file

    # Send a POST request to the desired URL
    print("Scrapping Successful")

# Schedule the task to run at intervals
schedule.every(0.1).minutes.do(run_check)

# Start a background thread to execute scheduled tasks
def background_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Check if the background thread has started
def check_background_thread():
    if not hasattr(app, 'background_thread') or not app.background_thread.is_alive():
        app.background_thread = threading.Thread(target=background_thread)
        app.background_thread.start()

@app.route('/', methods=['GET'])
def start_server():
    print("starting server")
    check_background_thread()  # Start the background thread if not already running
    return {"message": "server started successfully"}

@app.route('/receive-data', methods=['GET'])
def send_data():
    # Read the output.json file
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run()
