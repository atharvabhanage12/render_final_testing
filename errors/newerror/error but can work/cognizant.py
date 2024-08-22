####### . COMPANY CHANGED ITS WEBSITE
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

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

# Set up Chrome and ChromeDriver paths
chrome_binary_path = "/opt/render/project/src/chrome/chrome-linux64/chrome"
chrome_driver_path = "/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver"

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    logger.error(f"ChromeDriver not found at {chrome_driver_path}")
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://careers.cognizant.com/global-en/jobs/?keyword=&industry=Technology&location=India&radius=100&lat=&lng=&cname=India&ccode=IN&pagesize=10#results"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

L = []

# Function to collect job details
def collect_job_details():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find_all("li", class_='jobs-list-item')
    for job_element in job_elements:
        job_title = job_element.find("span", attrs={'data-ph-id':'ph-page-element-page2-28'}).text.strip()
        job_link = job_element.find("a", attrs={'data-ph-id':'ph-page-element-page2-24'})["href"]
        job_location = job_element.find("span", attrs={'data-ph-id':'ph-page-element-page2-31'}).text.strip()
        L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})

collect_job_details()
while True:
    try:
        element = driver.find_element(By.XPATH, "//span[@data-ph-id='ph-page-element-page2-077i6t-077i6t-100']")
        driver.execute_script("arguments[0].click()", element)
        time.sleep(3)
        collect_job_details()
    except Exception as e:
        logger.info("No more pages or an error occurred: {e}")
        break

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "cognizant", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")

