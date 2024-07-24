# gunicorn_config.py

# Set timeout to a very high value (e.g., 1 day = 86400 seconds)
timeout = 86400

# Alternatively, set timeout to 0 to disable it
timeout = 0

# Number of workers
workers = 4

# Log level
loglevel = 'info'

# Access log file
accesslog = '-'

# Error log file
errorlog = '-'
