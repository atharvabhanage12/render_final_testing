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
url = "https://www.hubspot.com/careers/jobs?hubs_signup-url=www.hubspot.com%2Fcareers&hubs_signup-cta=careers-homepage-hero&page=1#department=product-ux-engineering;"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
time.sleep(3)

# Click "Show all" button to load all job listings
try:
    show_all_button = driver.find_element(By.PARTIAL_LINK_TEXT, 'Show all')
    driver.execute_script("arguments[0].click()", show_all_button)
    logger.info("Clicked 'Show all' button")
    time.sleep(3)
except Exception as e:
    logger.error(f"Error clicking 'Show all' button: {e}")
    driver.quit()
    raise

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
jobs = soup.find_all("h3", class_="sc-htpNat jPYStQ")
locations = soup.find_all("p", class_="sc-ifAKCX gHfmgn")
links = soup.find_all("a", class_="sc-EHOje iHOrDr cta--primary cta--small careers-apply")
logger.info("Parsed job listings")

data = []
for i in range(len(jobs)):
    job_data = {
        "job_title": jobs[i].text,
        "job_location": locations[i].text,
        "job_link": "https://www.hubspot.com" + links[i]["href"]
    }
    data.append(job_data)

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "hubspot", "data": data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
