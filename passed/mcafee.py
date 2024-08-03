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
chrome_options.add_argument("--headless")  # Run headless if needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path

# Path to the manually downloaded ChromeDriver
chrome_driver_path = os.path.expanduser("/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver")
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
url = "https://careers.mcafee.com/global/en/search-results"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

L = []

# Select job categories
category = ['Engineering', 'Information Technology']
for i in category:
    try:
        team = driver.find_element(By.XPATH, f"//input[@type='checkbox' and @data-ph-at-text='{i}']")
        driver.execute_script('arguments[0].scrollIntoView();', team)
        driver.execute_script('arguments[0].click();', team)
        logger.info(f"Selected category: {i}")
        time.sleep(2)
    except Exception as e:
        logger.error(f"Error selecting category {i}: {e}")

# Get the total number of jobs
try:
    num_str = driver.find_element(By.XPATH, "//span[@class='result-count']").get_attribute('innerHTML')
    int_num = int(num_str)
    logger.info(f"Total jobs found: {int_num}")
except Exception as e:
    logger.error(f"Error retrieving total number of jobs: {e}")
    driver.quit()
    raise

# Scrape job listings
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("div", class_='job-title').text.strip()
        job_link = soup2.find("a")["href"]
        job_location = soup2.find('span', class_='au-target externalLocation').text.strip()
        job_category = soup2.find('span', class_='job-category').text[9:].strip()
        job_created = soup2.find('span', class_='job-postdate').text[12:].strip()
        L.append({"job_title": job_title, 'job_category': job_category, "job_link": job_link, "job_created": job_created, "job_location": job_location})
        logger.info(f"Collected job: {job_title} in {job_location}")
    try:
        elem = driver.find_element(By.XPATH, "//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except Exception as e:
        logger.info(f"No more pages to load or error encountered: {e}")
        break

    if len(L) >= int_num:
        break

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({'company': 'mcafee', 'data': L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
