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

logger.info("Starting Tesla scraping script")

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
    logger.info("WebDriver initialized for Tesla")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = 'https://www.tesla.com/careers/search/?region=5'
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

# Scroll down the page to load job listings
def scroll_down():
    """A method for scrolling the page."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_down()
soup = BeautifulSoup(driver.page_source, "html.parser")
logger.info("Page source obtained and parsed with BeautifulSoup")

# Extract job postings
category = ['Autopilot & Robotics', 'Engineering & Information Technology', 'Vehicle Software']
final_data = []
total = soup.find_all("tr", class_="tds-table-row")
total.pop(0)  # Remove the header row

for i in total:
    soup2 = BeautifulSoup(str(i), "html.parser")
    datasoup = soup2.find_all("td")
    job_title = datasoup[0].text
    job_link = 'https://www.tesla.com/' + datasoup[0].find('a')["href"]
    job_department = datasoup[1].text
    job_location = datasoup[2].text
    if job_department not in category:
        continue
    final_data.append({
        "job_title": job_title,
        "job_link": job_link,
        "job_department": job_department,
        "job_location": job_location
    })
    logger.info(f"Collected job: {job_title}, {job_department}, {job_location}, {job_link}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as outfile:
#     json.dump({"company": "tesla", "data": final_data}, outfile, indent=4)
# logger.info(f"Data saved to JSON: {output_path}")

print(final_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed for Tesla")
