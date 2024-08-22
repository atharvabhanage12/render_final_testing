import os
import logging
import json
import time
from selenium import webdriver
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

logger.info("Starting Unacademy scraping script")

# Set up Chrome options and ChromeDriver paths
chrome_binary_path = "/opt/render/project/src/chrome/chrome-linux64/chrome"
chrome_driver_path = os.path.expanduser("driver/chromedriver-mac-arm64/chromedriver")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.binary_location = chrome_binary_path

logger.info(f"ChromeDriver Path: {chrome_driver_path}")

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    logger.error(f"ChromeDriver not found at {chrome_driver_path}")
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)  # Ensure it's executable

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized for Unacademy")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://unacademy.darwinbox.in/ms/candidate/careers"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

# Wait for the page to load
driver.implicitly_wait(10)
time.sleep(2)

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
logger.info("Page source obtained and parsed with BeautifulSoup")

# Extract job postings
data = []
job_titles = soup.find_all("span", class_="css-8qk9uv")
job_locations = soup.find_all("div", class_="css-1cm4lgc")

for i in range(len(job_titles)):
    job_data = {
        "job_title": job_titles[i].text,
        "job_location": job_locations[i].text,
        "job_link": 'https://unacademy.skillate.com/'
    }
    data.append(job_data)
    logger.info(f"Collected job: {job_titles[i].text}, {job_locations[i].text}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as outfile:
#     json.dump({"company": "unacademy", "data": data}, outfile, indent=4)
# logger.info(f"Data saved to JSON: {output_path}")

print(data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed for Unacademy")
