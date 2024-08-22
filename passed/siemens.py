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
url = 'https://jobs.siemens.com/careers?pid=563156115868726&organization=Technology&domain=siemens.com&sort_by=relevance&triggerGoButton=false'
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

# Click "Show More" button to load all job postings
while True:
    try:
        elem = driver.find_element(By.XPATH, "//button[@class='btn btn-sm btn-secondary show-more-positions']")
        driver.execute_script('arguments[0].click();', elem)
        logger.info("Clicked 'Show More' button")
        time.sleep(2)
    except Exception as e:
        logger.info("No more 'Show More' button found or error encountered")
        break

# Parse job postings
soup = BeautifulSoup(driver.page_source, "html.parser")
job_elements = soup.find_all("div", class_="job-card-container list")
logger.info(f"Found {len(job_elements)} job postings")

job_list = []

for job in job_elements:
    soup2 = BeautifulSoup(str(job), "html.parser")
    # print(soup2)
    job_title = soup2.find("h3", class_='job-card-title').text.strip()
    # job_department = soup2.find("div", class_="row").text.strip()
    job_location = soup2.find("p").text.strip()
    job_link = 'https://jobs.siemens.com/careers'
    job_list.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
    logger.info(f"Collected job: {job_title} in {job_location}")

# Remove duplicates
unique_jobs = []
for job in job_list:
    if job not in unique_jobs:
        unique_jobs.append(job)
logger.info(f"Total unique jobs: {len(unique_jobs)}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "siemens", "data": unique_jobs}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

print(unique_jobs)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
