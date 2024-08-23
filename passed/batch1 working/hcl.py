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
url = "https://www.hcltech.com/careers/Careers-in-india#job-openings"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
time.sleep(3)

# Click "Load more items" until no more items are left
while True:
    try:
        elem = driver.find_element(By.XPATH, "//a[@title='Load more items']")
        driver.execute_script("arguments[0].click()", elem)
        time.sleep(3)
    except Exception as e:
        logger.info("No more items to load or error encountered.")
        break

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
jobs = soup.find_all("tr")
logger.info("Parsed job listings")

L = []
count = 0
for i in jobs:
    if count != 0:
        count += 1
        soup2 = BeautifulSoup(str(i), "html.parser")
        try:
            title = soup2.find("td", class_='views-field views-field-field-designation').text.replace("  ", " ")
            link = "https://www.hcltech.com" + soup2.find("a")["href"]
            location = soup2.find("td", class_='views-field views-field-field-kenexa-jobs-location').text.replace(" ", "")
            L.append({"job_title": title, "job_location": location, "job_link": link})
        except Exception as e:
            logger.error(f"Error parsing job listing: {e}")
    else:
        count += 1

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "hcl", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
