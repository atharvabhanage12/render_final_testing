import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

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

# Set up Chrome and ChromeDriver paths
chrome_binary_path = "/opt/render/project/src/chrome/chrome-linux64/chrome"
chrome_driver_path = "/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver"

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    logger.error(f"ChromeDriver not found at {chrome_driver_path}")
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://jobs.exxonmobil.com/search/?q=&department=engineering&sortColumn=referencedate&sortDirection=desc"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

job_data = []
page_number = 3
last_page = int(int(driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div[3]/div/div/div/span[1]/b[2]").text.strip()) / 25 + 2)

def collect_job_details():
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".searchResultsShell")))
    job_elements = driver.find_elements(By.CSS_SELECTOR, ".data-row")
    for job_element in job_elements:
        job_title = job_element.find_element(By.CSS_SELECTOR, '.colTitle').text.strip()
        job_location = job_element.find_element(By.CSS_SELECTOR, ".colLocation").text.strip()
        job_description = job_element.find_element(By.CSS_SELECTOR, ".jobDepartment").text.strip()
        job_details = {
            'job_title': job_title,
            'job_location': job_location,
            'job_category': job_description,
            "job_link": 'https://jobs.exxonmobil.com/'
        }
        job_data.append(job_details)

collect_job_details()
while True:
    try:
        page_number_element = driver.find_element(By.CSS_SELECTOR, f".pagination > li:nth-of-type({page_number}) a")
        page_number_element.click()
        page_number += 1
        time.sleep(3)
        collect_job_details()
        if page_number >= last_page:
            break
    except Exception as e:
        logger.info(f"No more pages or an error occurred: {e}")
        break

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "exxonmobil", "data": job_data}, f, indent=4)
logger.info(f"Data saved to JSON exonmobile: {output_path}")

# Close the browser
driver.quit()
logger.info("Driver quit, script completed")
