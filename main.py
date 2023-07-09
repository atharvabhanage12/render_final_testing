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

async def run_check():
    # Execute check.py using subprocess
    print("Running process...")
    await subprocess.run(['python', 'check.py'])
    print("Scraping completed")

def install_chrome():
    result = subprocess.run(['python','temp.py'])
    # print(result.stdout)

# run_check()
install_chrome()

# @app.route('/setupbrowser',methods=['GET'])
# def setupbrowser():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_in_executor(executor, install_chrome)
#     return {"message": "Browser Installation Started"}
async def scrape():
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.run_in_executor(executor, run_check)
    asyncio.create_task(run_check())
@app.route('/cronjob', methods=['GET'])
def run_task():
    asyncio.run(scrape())
    return {"message": "Pinged server successfully"}





@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as a JSON response
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
