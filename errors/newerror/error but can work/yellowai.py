import os
import logging
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("yellowai_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting Yellow.ai scraping script")

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
    logger.info("WebDriver initialized for Yellow.ai")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://yellow-ai.sensehq.com/careers"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

# Wait for the page to load
driver.implicitly_wait(10)

# Scroll down to load all job postings
driver.execute_script("window.scrollTo(0, 0.95 * document.body.scrollHeight);")
time.sleep(3)

# Initialize job list
final_data = []

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
fields = soup.find_all("div", class_="postings-group")

# Filter and collect job data
job_elements = []
for field in fields:
    category = field.find("div", class_="posting-category-title large-category-label").text
    if category in ["Infosec", "Technical Support"]:
        job_elements.extend(field.find_all("a", class_="posting-title"))

for job_element in job_elements:
    soup2 = BeautifulSoup(str(job_element), "html.parser")
    job_link = soup2.find("a")["href"]
    job_title = soup2.find("h5").text
    job_location = soup2.find("span", class_="sort-by-location posting-category small-category-label location").text
    final_data.append({
        "job_title": job_title,
        "job_location": job_location,
        "job_link": job_link
    })
    logger.info(f"Collected job: {job_title}, {job_location}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/yellowai_jobs.json"
# with open(output_path, "w") as outfile:
#     json.dump({"company": "yellowai", "data": final_data}, outfile, indent=4)
# logger.info(f"Data saved to JSON: {output_path}")

print(final_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed for Yellow.ai")
