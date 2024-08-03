# ###### Getting error in this code 

# Traceback (most recent call last):
#   File "/Users/atharvabhanage/Desktop/joble/webscrapeJoble/render_final_testing/errors/passed/jpmorgan.py", line 68, in <module>
#     element = driver.find_element(By.XPATH, "//a[@class='filter-menu-dropdown-click']")
#               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 831, in find_element
#     return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 440, in execute
#     self.error_handler.check_response(response)
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/errorhandler.py", line 245, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//a[@class='filter-menu-dropdown-click']"}
#   (Session info: chrome=127.0.6533.73)
# Stacktrace:
# 0   chromedriver                        0x00000001046b2a0c chromedriver + 4385292
# 1   chromedriver                        0x00000001046ab318 chromedriver + 4354840
# 2   chromedriver                        0x00000001042c8b0c chromedriver + 281356
# 3   chromedriver                        0x000000010430b2f8 chromedriver + 553720
# 4   chromedriver                        0x0000000104343d24 chromedriver + 785700
# 5   chromedriver                        0x00000001042ffeec chromedriver + 507628
# 6   chromedriver                        0x00000001043008c4 chromedriver + 510148
# 7   chromedriver                        0x000000010467a3c8 chromedriver + 4154312
# 8   chromedriver                        0x000000010467ee2c chromedriver + 4173356
# 9   chromedriver                        0x000000010465ff84 chromedriver + 4046724
# 10  chromedriver                        0x000000010467f718 chromedriver + 4175640
# 11  chromedriver                        0x0000000104652f44 chromedriver + 3993412
# 12  chromedriver                        0x000000010469d1a8 chromedriver + 4297128
# 13  chromedriver                        0x000000010469d324 chromedriver + 4297508
# 14  chromedriver                        0x00000001046aaf10 chromedriver + 4353808
# 15  libsystem_pthread.dylib             0x000000018dccef94 _pthread_start + 136
# 16  libsystem_pthread.dylib             0x000000018dcc9d34 thread_start + 8

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
url = "https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/requisitions?keyword="
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)

# Apply filters
try:
    element = driver.find_element(By.XPATH, "//a[@class='filter-menu-dropdown-click']")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)
    element = driver.find_element(By.XPATH, "//a[@data-filter-tag='Technology']")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)
    element = driver.find_element(By.XPATH, "//label[@for='aoi__Technology__Technology']")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(3)
    logger.info("Filters applied")
except Exception as e:
    logger.error(f"Error applying filters: {e}")
    driver.quit()
    raise

# Function to scrape job listings
def continue_code(driver, classo, idx):
    global L
    ele = driver.find_elements(By.XPATH, "//p[@class='moduleTitle']")
    driver.execute_script("arguments[0].click();", ele[idx])
    time.sleep(4)
    current_html = driver.page_source
    soup = BeautifulSoup(current_html, "html.parser")
    job_elements = soup.find_all("div", class_=classo)
    driver.execute_script("window.scrollTo(0, 0.80 * document.body.scrollHeight);")
    for i in job_elements:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("p", class_='type').text
        job_location = soup2.find("p", class_='location-name').text
        job_link = "https://careers.jpmorgan.com" + soup2.find("a", class_='event-name-href')["href"]
        job_description = soup2.find("p", class_='external-description').text.replace("\n", " ")
        L.append({"job_title": job_title, "job_description": job_description, "job_location": job_location, "job_link": job_link})
    driver.execute_script("window.scrollTo(0, 0.30 * document.body.scrollHeight);")
    logger.info(f"Scraped {len(job_elements)} jobs from section {classo}")

L = []
continue_code(driver, "filter-display-card programs school active", 0)
continue_code(driver, "filter-display-card programs preinternship active", 1)
continue_code(driver, "filter-display-card programs internship active", 2)
continue_code(driver, "filter-display-card programs fulltime active", 3)

logger.info(f"Total jobs scraped: {len(L)}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "jpmorgan", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

print(L)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
