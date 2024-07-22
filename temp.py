import os
import time
import subprocess

# Run the script and capture the output
result = subprocess.run(['./script.sh'], capture_output=True, text=True)

# Print the captured stdout and stderr
print("ATHARVA DEBUG: script.sh output")
print(result.stdout)
print(result.stderr)

chromium_path = "/opt/render/chrome/chrome-linux64/chrome"
print("ATHARVA DEBUG: chromium_path")
print(chromium_path)

# Add the Chromium path to the PATH environment variable
os.environ['PATHCHROME'] = chromium_path
os.environ["PATH"] += ":" + chromium_path

# Verify the updated PATH
print("ATHARVA DEBUG: Updated PATH")
print(os.environ['PATH'])

time.sleep(4)
