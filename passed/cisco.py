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
url = "https://jobs.cisco.com/jobs/SearchJobs/?21181=%5B186%2C194%2C187%2C191%2C202%2C185%2C55816092%5D&21181_format=6023&listFilterMode=1"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

# Close the cookie banner if present
try:
    driver.find_element(By.XPATH, "//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
    logger.info("Closed cookie banner")
except Exception as e:
    logger.info("No cookie banner to close")

# Script to extract job links
script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i < elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""

# Function to collect job details
def collect_job_details():
    job_links = driver.execute_script(script)
    hrefs = [i for i in job_links if "/ProjectDetail/" in i]
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find("tbody").find_all("tr")
    jobs = []
    for i, job in enumerate(job_elements):
        soup2 = BeautifulSoup(str(job), "html.parser")
        job_title = soup2.find("td", attrs={"data-th": "Job Title"}).text.strip()
        job_link = hrefs[i]
        job_location = soup2.find("td", attrs={"data-th": "Location"}).text.strip()
        jobs.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
    return jobs

# Collect all job listings with pagination
all_jobs = []
while True:
    jobs = collect_job_details()
    all_jobs.extend(jobs)
    try:
        next_button = driver.find_element(By.XPATH, "//a[@class='pagination_item'][contains(text(), '>>')]")
        driver.execute_script("arguments[0].click()", next_button)
        time.sleep(3)
    except:
        break

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "cisco", "data": all_jobs}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
