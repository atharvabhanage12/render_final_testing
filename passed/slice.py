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

logger.info("Starting Slice scraping script")

# Set up Chrome options and ChromeDriver paths
chrome_binary_path = "/opt/render/project/src/chrome/chrome-linux64/chrome"
chrome_driver_path = os.path.expanduser("/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path

logger.info(f"ChromeDriver Path: {chrome_driver_path}")

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    logger.error(f"ChromeDriver not found at {chrome_driver_path}")
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)  # Ensure it's executable

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized for Slice")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://careers.smartrecruiters.com/slice1"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

# Scroll down the page to load job listings
driver.execute_script("window.scrollTo(0, 0.95 * document.body.scrollHeight);")
time.sleep(3)

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
logger.info("Page source obtained and parsed with BeautifulSoup")

final_data = []
fields = soup.find_all("section", class_="openings-section opening opening--grouped js-group")

for field in fields:
    if field.find("h3").text == "Engineering":
        job_elements = field.find_all("li", class_="opening-job job column wide-7of16 medium-1of2")

        for i in job_elements:
            soup2 = BeautifulSoup(str(i), "html.parser")
            job_link = soup2.find("a")["href"]
            job_title = soup2.find("h4").text
            job_location = "Bengaluru, Karnataka, India"
            final_data.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
            logger.info(f"Collected job: {job_title}, {job_location}, {job_link}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as outfile:
    json.dump({"company": "slice", "data": final_data}, outfile, indent=4)
logger.info(f"Data saved to JSON slice: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed for Slice")
