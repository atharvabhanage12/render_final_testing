import asyncio
from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor
import json
import subprocess
from waitress import serve
import os
import time

app = Flask(__name__)
executor = ThreadPoolExecutor()

def run_check():
    # Execute check.py using subprocess
    print("Running process...")
    subprocess.run(['python', 'check.py'])
    print("Scraping completed")

def install_chrome():
    result = subprocess.rin(['python','temp.py'])
    print(result.stdout)

# run_check()

@app.route('/setupbrowser',methods=['GET'])
def setupbrowser():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(executor, install_chrome)
    return {"message": "Browser Installation Started"}

@app.route('/cronjob', methods=['GET'])
def scrape():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(executor, run_check)
    return {"message": "Pinged server successfully"}





@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as a JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)
