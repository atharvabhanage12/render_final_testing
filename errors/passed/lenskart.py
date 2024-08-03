######## GIGINVG ERROR 


# Traceback (most recent call last):
#   File "/Users/atharvabhanage/Desktop/joble/webscrapeJoble/render_final_testing/errors/passed/lenskart.py", line 71, in <module>
#     tech_ele = driver.find_element(By.XPATH, "//select[@id='department']")
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 831, in find_element
#     return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 440, in execute
#     self.error_handler.check_response(response)
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/errorhandler.py", line 245, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//select[@id='department']"}

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
url = "https://hiring.lenskart.com/jobs-demp2"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

L = []

# Interact with the webpage
try:
    tech_ele = driver.find_element(By.XPATH, "//select[@id='department']")
    driver.execute_script("arguments[0].click();", tech_ele)
    sub_tech_ele = driver.find_element(By.XPATH, "//option[@value='Technology']")
    driver.execute_script("arguments[0].click();", sub_tech_ele)
    logger.info("Selected Technology department")
except Exception as e:
    logger.error(f"Error interacting with the webpage: {e}")
    driver.quit()
    raise

time.sleep(3)

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
tech_elem = soup.find_all("a", class_='job job__row')
for i in tech_elem:
    soup2 = BeautifulSoup(str(i), "html.parser")
    job_title = soup2.find("h5", class_='title').text.replace("\n", "")
    job_location = soup2.find("span", class_='location').text.replace("\n", "")
    job_link = "https://hiring.lenskart.com" + i["href"]
    L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
    logger.info(f"Collected job: {job_title} in {job_location}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "lenskart", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

print(L)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
