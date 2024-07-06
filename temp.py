import os
import time
import subprocess
result = subprocess.run(['./script.sh'], capture_output=True, text=True)
chromium_path = result.stdout.strip()

print(" ATHARVA DEBUG chromium_path")
print(result.stderr)

# Add the Chromium path to the PATH environment variable
os.environ['PATHCHROME'] =  chromium_path
os.environ["PATH"]+=":"+chromium_path

# Verify the updated PATsH
print("ATHARVA DEBUG checking just")
print(os.environ['PATH'])

time.sleep(4)

