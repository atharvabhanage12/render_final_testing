### Can we fixed
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
url = "https://juspay.in/careers"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
driver.execute_script("window.scrollTo(0, 0.95 * document.body.scrollHeight);")
time.sleep(3)

final_data = []

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
fields = soup.find_all("article", class_="openings__category")
for field in fields:
    if field.find("h1").text == "Engineering":
        job_elements = field.find_all("article", class_="opening__desc")
        for job in job_elements:
            soup2 = BeautifulSoup(str(job), "html.parser")
            job_link = "https://juspay.in" + soup2.find("a")["href"]
            job_title = soup2.find("h4").text
            job_location = soup2.find("article", class_="opening__location").text
            final_data.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "juspay", "data": final_data}, f, indent=4)
# logger.info(f"Data saved to JSON: {output_path}")
print(final_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
