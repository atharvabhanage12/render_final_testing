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
website = "https://www.janestreet.com/join-jane-street/open-roles/?type=students-and-new-grads&location=all-locations&department=technology"
try:
    driver.get(website)
    logger.info(f"Accessed URL: {website}")
except Exception as e:
    logger.error(f"Error accessing URL {website}: {e}")
    driver.quit()
    raise

time.sleep(4)

# Parse the job listings
soup = BeautifulSoup(driver.page_source, 'html.parser')
job_div = soup.find('div', class_='jobs-container row')
jobs = job_div.find_all('a')
logger.info("Parsed job listings")

job_data = []

for job in jobs:
    link = 'https://www.janestreet.com' + job['href']
    title = job.find('div', class_='item students-and-new-grads position').get_text()
    location = job.find('div', class_='item students-and-new-grads city').get_text()

    try:
        driver.get(link)
        logger.info(f"Accessed job link: {link}")
        time.sleep(5)
        about = driver.find_element(By.XPATH, '//div[@class="job-content row"]').text
        job_data.append({
            'job_title': title,
            'job_location': location,
            'job_link': link,
            'job_desc': about
        })
    except Exception as e:
        logger.error(f"Error accessing job link {link}: {e}")

driver.quit()
logger.info("Driver quit, data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "jane_street", "data": job_data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")
