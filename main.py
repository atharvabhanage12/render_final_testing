import time
import os
import requests
from flask import Flask, jsonify,request
import json
import subprocess
import signal
import sys
from waitress import serve
import requests
app = Flask(__name__)




@app.route('/update_output', methods=['POST'])
def update_output():
    # Check if a file is included in the request
    if 'output.json' not in request.files:
        return 'No file provided', 400

    file = request.files['output.json']

    # # Check if output.json already exists
    if os.path.exists('output.json'):
        os.remove('output.json')

    # Save the file to the server's folder
    file.save('output.json')
    
    return 'File uploaded and replaced successfully'

@app.route('/receive-data', methods=['GET'])
def send_data():
    with open('output.json', 'r') as file:
        data = json.load(file)
    
    # Return the data as JSON response
    return jsonify(data)

if __name__ == '__main__':
    # Run the Flask app
    app.run()
