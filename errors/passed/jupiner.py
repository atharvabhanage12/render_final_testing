# #######GIGING SOME ERROR 
# Accessed URL: https://careers.juniper.net/#/
# Traceback (most recent call last):
#   File "/Users/atharvabhanage/Desktop/joble/webscrapeJoble/render_final_testing/errors/passed/jupiner.py", line 72, in <module>
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-group")))
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/support/wait.py", line 95, in until
#     raise TimeoutException(message, screen, stacktrace)
# selenium.common.exceptions.TimeoutException: Message: 
# Stacktrace:
# 0   chromedriver                        0x00000001009c2a0c chromedriver + 4385292
# 1   chromedriver                        0x00000001009bb318 chromedriver + 4354840
# 2   chromedriver                        0x00000001005d8b0c chromedriver + 281356
# 3   chromedriver                        0x000000010061b2f8 chromedriver + 553720
# 4   chromedriver                        0x0000000100653d24 chromedriver + 785700
# 5   chromedriver                        0x000000010060feec chromedriver + 507628
# 6   chromedriver                        0x00000001006108c4 chromedriver + 510148
# 7   chromedriver                        0x000000010098a3c8 chromedriver + 4154312
# 8   chromedriver                        0x000000010098ee2c chromedriver + 4173356
# 9   chromedriver                        0x000000010096ff84 chromedriver + 4046724
# 10  chromedriver                        0x000000010098f718 chromedriver + 4175640
# 11  chromedriver                        0x0000000100962f44 chromedriver + 3993412
# 12  chromedriver                        0x00000001009ad1a8 chromedriver + 4297128
# 13  chromedriver                        0x00000001009ad324 chromedriver + 4297508
# 14  chromedriver                        0x00000001009baf10 chromedriver + 4353808
# 15  libsystem_pthread.dylib             0x000000018dccef94 _pthread_start + 136
# 16  libsystem_pthread.dylib             0x000000018dcc9d34 thread_start + 8

# atharvabhanage@Atharvas-MacBook-Air render_final_testing % 

import os
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting script")

chrome_binary_path = "/opt/render/project/src/chrome/chrome-linux64/chrome"
# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run headless if needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.binary_location = chrome_binary_path

# Path to the manually downloaded ChromeDriver
chrome_driver_path = os.path.expanduser("driver/chromedriver-mac-arm64/chromedriver")
logger.info(f"ChromeDriver Path: {chrome_driver_path}")

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    logger.error(f"ChromeDriver not found at {chrome_driver_path}")
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)  # Ensure it's executable

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
website = "https://careers.juniper.net/#/"
try:
    driver.get(website)
    logger.info(f"Accessed URL: {website}")
except Exception as e:
    logger.error(f"Error accessing URL {website}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
driver.maximize_window()

# Scrape job listings
job_data = []

while True:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".list-group")))

    job_elements = driver.find_elements(By.CSS_SELECTOR, ".list-group-item")

    for job_element in job_elements:
        try:
            title_element = job_element.find_element(By.CSS_SELECTOR, '.list-group-item > p:nth-of-type(1) > b')
            job_title = title_element.text.strip()
        except Exception as e:
            job_title = "Not available"
            logger.error(f"Error extracting job title: {e}")

        try:
            location_element = job_element.find_element(By.CSS_SELECTOR, ".list-group-item > p:nth-of-type(2)")
            job_location = location_element.text.strip()
        except Exception as e:
            job_location = "Location not available"
            logger.error(f"Error extracting job location: {e}")

        job_details = {
            'job_title': job_title,
            'job_location': job_location,
            'job_link': 'https://careers.juniper.net/#/'
        }

        job_data.append(job_details)

    try:
        next_button = driver.find_element(By.CSS_SELECTOR, ".pagination > li:nth-last-child(2)")
        if 'disabled' in next_button.get_attribute('class'):
            break
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)
    except Exception as e:
        logger.info("No more pages to navigate or error encountered")
        break

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "juniper", "data": job_data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

print(job_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
