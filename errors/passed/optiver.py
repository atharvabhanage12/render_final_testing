# ###### having ERROR 
# Traceback (most recent call last):
#   File "/Users/atharvabhanage/Desktop/joble/webscrapeJoble/render_final_testing/errors/passed/optiver.py", line 70, in <module>
#     select_element = driver.find_element(by=By.XPATH, value='//select[@data-placeholder="Departments"]')
#                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 831, in find_element
#     return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
#            ^^^^^^^^^^^^^^^
# self.error_handler.check_response(response)
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/errorhandler.py", line 245, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//select[@data-placeholder="Departments"]



import os
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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

# Navigate to the website
website = "https://optiver.com/working-at-optiver/career-opportunities/#roles"
try:
    driver.get(website)
    logger.info(f"Accessed URL: {website}")
except Exception as e:
    logger.error(f"Error accessing URL {website}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
time.sleep(3)

# Select the Technology department
try:
    select_element = driver.find_element(by=By.XPATH, value='//select[@data-placeholder="Departments"]')
    select = Select(select_element)
    select.select_by_visible_text('Technology')
    logger.info("Selected Technology department")
    time.sleep(2)
except Exception as e:
    logger.error(f"Error selecting Technology department: {e}")
    driver.quit()
    raise

links_set = set()

# Collect job links
while True:
    try:
        links = driver.find_elements(By.CLASS_NAME, 'h5')
        for li in links:
            links_set.add(li.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        load_more_button = driver.find_element(By.XPATH, '//div[@class="row loadmore"]').find_element(By.TAG_NAME, 'a')
        if not load_more_button.is_displayed():
            break

        driver.execute_script('arguments[0].click()', load_more_button)
        logger.info("Clicked load more button")
        time.sleep(3)
    except Exception as e:
        logger.error(f"Error during job link collection: {e}")
        break

job_data = []

# Collect job details
for link in links_set:
    try:
        driver.get(link)
        time.sleep(3)
        title = driver.find_element(By.TAG_NAME, 'h1').text
        location = driver.find_element(By.XPATH, '//div[@class="bottom"]').find_element(By.TAG_NAME, 'p').text
        about = driver.find_element(By.TAG_NAME, 'section').text
        job_data.append({'job_title': title, 'job_location': location, 'job_link': link, 'job_desc': about})
        logger.info(f"Collected job: {title} in {location}")
    except Exception as e:
        logger.error(f"Error collecting job details: {e}")
        continue

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "optiver", "data": job_data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")
print(job_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
