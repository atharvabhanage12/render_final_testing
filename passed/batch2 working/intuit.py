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
url = "https://jobs.intuit.com/search-jobs/"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(15)

# Open category filter
try:
    element_filter = driver.find_element(By.XPATH, "//button[@id='category-toggle']")
    element_filter.click()
    logger.info("Opened category filter")
except Exception as e:
    logger.error(f"Error opening category filter: {e}")
    driver.quit()
    raise

# Get filter elements
initial_html = driver.page_source
soup = BeautifulSoup(initial_html, "html.parser")
filter_elements = soup.find_all("span", class_='filter__facet-name')

filters = ["Data", "Information Technology", "Software Engineering"]
L1 = [i for i in filter_elements if i.text in filters]
L2 = [str(i.parent['for']) for i in L1]

# Apply filters
for i in L2:
    time.sleep(3)
    try:
        driver.find_element(By.XPATH, f"//label[@for='{i}']").click()
        logger.info(f"Applied filter: {i}")
    except Exception as e:
        logger.error(f"Error applying filter {i}: {e}")

# Close category filter
try:
    element_filter = driver.find_element(By.XPATH, "//button[@id='category-toggle']")
    element_filter.click()
    logger.info("Closed category filter")
    time.sleep(3)
except Exception as e:
    logger.error(f"Error closing category filter: {e}")
    driver.quit()
    raise

# Get the total number of pages
try:
    x = int(driver.find_element(By.XPATH, "//span[@class='pagination-total-pages']").text[2:])
    logger.info(f"Total number of pages: {x}")
except Exception as e:
    logger.error(f"Error getting total number of pages: {e}")
    driver.quit()
    raise

L = []

# Scrape job listings with pagination
for i in range(x):
    time.sleep(4)
    updated_html = driver.page_source
    soup = BeautifulSoup(updated_html, "html.parser")
    job_elements = soup.find_all("a", class_='sr-item')
    for j in job_elements:
        soup2 = BeautifulSoup(str(j), "html.parser")
        try:
            job_title = soup2.find("h2").text
            job_location = soup2.find("span", class_='job-location').text
            job_link = url + str(soup2.find("a", class_='sr-item')["href"][1:])
            job_data = {
                "job_title": job_title,
                "job_location": job_location,
                "job_link": job_link
            }
            if job_data not in L:
                L.append(job_data)
        except Exception as e:
            logger.error(f"Error parsing job element: {e}")

    if i != x - 1:
        try:
            driver.find_element(By.XPATH, "//a[@class='next']").click()
            logger.info("Navigated to next page")
        except Exception as e:
            try:
                driver.implicitly_wait(20)
                element = driver.find_element(By.XPATH, "//a[@class='next']")
                driver.execute_script("arguments[0].click();", element)
                logger.info("Navigated to next page with JavaScript")
            except Exception as e:
                logger.error(f"Error navigating to next page: {e}")
                break

    driver.implicitly_wait(30)

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "intuit", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
