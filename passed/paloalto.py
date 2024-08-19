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
url = "https://jobs.paloaltonetworks.com/en/jobs/?department=Engineering&department=Information+Security&department=Information+Technology&pagesize=20#results"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i< elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""

L = []

def function1():
    L1 = driver.execute_script(script)
    hrefs = [i for i in L1 if "/en/jobs/job/" in i]
    count = 0
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find_all("div", class_='card card-job')
    for i in job_elements:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("h2").text.strip()
        job_link = hrefs[count]
        job_location = soup2.find("li", class_='list-inline-item').text.strip()
        L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
        logger.info(f"Collected job: {job_title} in {job_location}")
        count += 1

while True:
    function1()
    try:
        element = driver.find_element(By.XPATH, "//a[@aria-label='Go to next page of results']")
        driver.execute_script("arguments[0].click()", element)
        logger.info("Clicked next page")
        time.sleep(2)
    except Exception as e:
        logger.info(f"No more pages to load or error encountered: {e}")
        break

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "paloalto", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
