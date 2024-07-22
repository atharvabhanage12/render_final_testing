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
import requests
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

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

logger.info("Starting script")
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
url = "https://www.yahooinc.com/careers/search.html"
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
soup = BeautifulSoup(driver.page_source, "html.parser")
logger.info("Page source obtained and parsed with BeautifulSoup")

# Expand the job categories
try:
    var0 = driver.find_element(By.XPATH, "//button[@data-target='#collapseJC']")
    driver.execute_script("arguments[0].click()", var0)
    logger.info("Expanded job categories")
except Exception as e:
    logger.error(f"Error expanding job categories: {e}")
    driver.quit()
    raise

time.sleep(2)

# Select specific job categories
job_categories = ["engineering", "softwaredevelopment", "design", "informationsystems", "internship", "research"]
for category in job_categories:
    try:
        checkbox = driver.find_element(By.ID, category)
        driver.execute_script("arguments[0].click()", checkbox)
        logger.info(f"Selected category: {category}")
    except Exception as e:
        logger.error(f"Error selecting category {category}: {e}")

# Submit the job search form
try:
    submit = driver.find_element(By.XPATH, "//button[@id='search-page-find-jobs']")
    driver.execute_script("arguments[0].click()", submit)
    logger.info("Submitted job search form")
except Exception as e:
    logger.error(f"Error submitting search form: {e}")
    driver.quit()
    raise

time.sleep(3)

# Load more results if available
previous_count = 0
while True:
    try:
        load_more = driver.find_element(By.XPATH, "//button[@class='btn my-3 loadMore']")
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(2)
        
        # Get the current number of job listings
        soup2 = BeautifulSoup(driver.page_source, "html.parser")
        total = soup2.find_all("tr", class_='jobTitle')
        current_count = len(total)
        
        # Check if the number of listings has increased
        if current_count == previous_count:
            break
        previous_count = current_count
        logger.info(f"Loaded more results: {current_count} jobs")
    except Exception as e:
        # If the "Load More" button is not found, exit the loop
        logger.info(f"No more results to load or error encountered: {e}")
        break

# Parse the job listings
soup2 = BeautifulSoup(driver.page_source, "html.parser")
total = soup2.find_all("tr", class_='jobTitle')
logger.info("Parsed job listings")

# Extract job links
script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i < elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""
L1 = driver.execute_script(script)
hrefs = [i for i in L1 if "/careers/job/" in i]

# Collect job data
count = 0
for job in total:
    soup3 = BeautifulSoup(str(job), "html.parser")
    job_title = soup3.find("td", class_='col-6').text.strip()
    job_link = hrefs[count]
    job_location = soup3.find("div", class_="tableLocPrimary").text.strip()
    L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
    count += 1

logger.info("Data collection complete")
# Save the data as JSON
json_data = json.dumps({"company": "yahoo", "data": L}, indent=4)
logger.info("Data saved to JSON")
print(json_data)

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
