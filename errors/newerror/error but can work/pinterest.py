##### ERRORRRR:::  WEBSITE DSIGN CHANGED #####


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
url = "https://www.pinterestcareers.com/job-search-results/?primary_category=Engineering"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
time.sleep(3)

job_list = []
link_list = []

# Function to scrape job data from the current page
def scrape_jobs():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs = soup.find_all("a", id=lambda x: x and x.startswith("job-result"))
    for job in jobs:
        job_title = job.text
        job_link = "https://www.pinterestcareers.com" + job["href"]
        job_list.append(job_title)
        link_list.append(job_link)
        logger.info(f"Collected job: {job_title}")

# Scrape jobs from the first page
scrape_jobs()

# Navigate to the second page and scrape jobs
try:
    next_button = driver.find_element(By.XPATH, "//a[@id='pagination2']")
    driver.execute_script("arguments[0].click();", next_button)
    logger.info("Clicked next page button")
    time.sleep(3)
    scrape_jobs()
except Exception as e:
    logger.info(f"No more pages to load or error encountered: {e}")

# Compile the job data
data = []
for i in range(len(job_list)):
    job_data = {
        "job_title": job_list[i],
        "job_link": link_list[i],
        "job_location": 'unknown'
    }
    data.append(job_data)

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "pinterest", "data": data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")
print(data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
