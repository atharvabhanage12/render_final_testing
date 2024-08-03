# #####Giving some error 

# Traceback (most recent call last):
#   File "/Users/atharvabhanage/Desktop/joble/webscrapeJoble/render_final_testing/errors/passed/imc.py", line 80, in <module>
#     category = driver.find_element(By.XPATH, "//input[@type='checkbox' and @data-ph-at-text='Technology']")
#                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 831, in find_element
#     return self.execute(Command.FIND_ELEMENT, {"using": by, "value": value})["value"]
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 440, in execute
#     self.error_handler.check_response(response)
#   File "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/selenium/webdriver/remote/errorhandler.py", line 245, in check_response
#     raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element: {"method":"xpath","selector":"//input[@type='checkbox' and @data-ph-at-text='Technology']"}
#   (Session info: chrome=127.0.6533.73)
# Stacktrace:
# 0   chromedriver                        0x0000000104a62a0c chromedriver + 4385292
# 1   chromedriver                        0x0000000104a5b318 chromedriver + 4354840
# 2   chromedriver                        0x0000000104678b0c chromedriver + 281356
# 3   chromedriver                        0x00000001046bb2f8 chromedriver + 553720
# 4   chromedriver                        0x00000001046f3d24 chromedriver + 785700
# 5   chromedriver                        0x00000001046afeec chromedriver + 507628
# 6   chromedriver                        0x00000001046b08c4 chromedriver + 510148
# 7   chromedriver                        0x0000000104a2a3c8 chromedriver + 4154312
# 8   chromedriver                        0x0000000104a2ee2c chromedriver + 4173356
# 9   chromedriver                        0x0000000104a0ff84 chromedriver + 4046724
# 10  chromedriver                        0x0000000104a2f718 chromedriver + 4175640
# 11  chromedriver                        0x0000000104a02f44 chromedriver + 3993412
# 12  chromedriver                        0x0000000104a4d1a8 chromedriver + 4297128
# 13  chromedriver                        0x0000000104a4d324 chromedriver + 4297508
# 14  chromedriver                        0x0000000104a5af10 chromedriver + 4353808
# 15  libsystem_pthread.dylib             0x000000018dccef94 _pthread_start + 136
# 16  libsystem_pthread.dylib             0x000000018dcc9d34 thread_start + 8

# atharvabhanage@At






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
url = "https://careers.imc.com/in/en/search-results"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

# Accept cookies
try:
    cookies = driver.find_element(By.XPATH, "//button[@class='btn primary-button au-target' and @click.delegate='acceptAndClose()']")
    driver.execute_script('arguments[0].click();', cookies)
    logger.info("Accepted cookies")
    time.sleep(2)
except Exception as e:
    logger.error(f"Error accepting cookies: {e}")
    driver.quit()
    raise

# Select 'Technology' category
try:
    category = driver.find_element(By.XPATH, "//input[@type='checkbox' and @data-ph-at-text='Technology']")
    driver.execute_script('arguments[0].click();', category)
    logger.info("Selected 'Technology' category")
    time.sleep(2)
except Exception as e:
    logger.error(f"Error selecting 'Technology' category: {e}")
    driver.quit()
    raise

# Get the total number of jobs
try:
    num_str = driver.find_element(By.XPATH, "//span[@class='result-count']").get_attribute('innerHTML')
    int_num = int(num_str)
    logger.info(f"Total number of jobs: {int_num}")
except Exception as e:
    logger.error(f"Error getting total number of jobs: {e}")
    driver.quit()
    raise

L = []

# Scrape job listings with pagination
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        try:
            job_title = soup2.find(attrs={'data-ph-id': "ph-default-1544535895472-ph-search-results-v2073sfp-q7xTkZ"}).text
            job_link = soup2.find("a", class_="au-target")["href"]
            job_requirements = soup2.find(attrs={'data-ph-id': "ph-default-1544535895472-ph-search-results-v2073sfp-bPhXdP"}).text.strip()
            job_location = soup2.find("span", class_="job-location").text.strip()[11:]
            job_commitment = soup2.find("span", class_="au-target type").text.strip()
            L.append({
                "job_title": job_title,
                "job_link": job_link,
                "job_requirements": job_requirements,
                "job_location": job_location,
                "job_commitment": job_commitment
            })
        except Exception as e:
            logger.error(f"Error parsing job listing: {e}")

    try:
        elem = driver.find_element(By.XPATH, "//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        logger.info("Navigated to next page")
        time.sleep(2)
    except Exception as e:
        logger.info("No more pages to navigate or error encountered")
        break

    if len(L) >= int_num:
        logger.info("Collected all job listings")
        break

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
    # json.dump({'company': 'imc trading', 'data': L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

print(L)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
