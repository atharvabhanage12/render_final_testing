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
url = 'https://jobs.gartner.com/jobs/?search=&department=Technology&contractType=&pagesize=20'
job_department = 'Technology'
L = []

try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

def collect_job_details():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find_all("div", class_="card-body")
    for job_element in job_elements:
        job_title = job_element.find("a").text.strip()
        job_link = 'https://jobs.gartner.com' + job_element.find("a")["href"]
        job_location = job_element.find("li", class_="list-inline-item").text.strip()
        L.append({"job_title": job_title, "job_link": job_link, "job_department": job_department, "job_location": job_location})

collect_job_details()
while True:
    try:
        next_button = driver.find_element(By.XPATH, "//a[@aria-label='Go to next page of results']")
        driver.execute_script('arguments[0].click();', next_button)
        time.sleep(2)
        collect_job_details()
    except Exception as e:
        logger.info(f"No more pages or an error occurred: {e}")
        break

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({'company': 'gartner', 'data': L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Close the browser
driver.quit()
logger.info("Driver quit, script completed")
