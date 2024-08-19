
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

# Navigate to the website
url = "https://jobs.careers.microsoft.com/global/en/search?p=Software%20Engineering&p=Data%20Center&p=Research%2C%20Applied%2C%20%26%20Data%20Sciences&p=Hardware%20Engineering&p=Engineering&p=Design%20%26%20Creative&p=Analytics&p=Technical%20Support&d=Art&d=Software%20Engineering&rt=People%20Manager&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.maximize_window()
driver.implicitly_wait(10)

job_data = []

while True:
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ms-List-page")))

        # Get all the job elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".ms-List-cell")

        # Iterate over the job elements and extract the job information
        for job_element in job_elements:
            # Extract job title
            title_element = job_element.find_element(By.CSS_SELECTOR, '.MZGzlrn8gfgSs8TZHhv2')
            job_title = title_element.text.strip()

            # Extract job location
            location_element = job_element.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[10]/div/div/div[2]/div[1]/div/div/div[2]/span")
            job_location = location_element.text.strip()
           
            job_details = {
                'job_title': job_title,
                'job_location': job_location,
                'job_link': 'https://careers.microsoft.com/v2/global/en/home.html'
            }

            # Append the job details to the job data list
            job_data.append(job_details)
            logger.info(f"Collected job: {job_title} in {job_location}")

        # Check if there's a next button
        next_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[5]/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/div/div[3]/button")
        if 'disabled' in next_button.get_attribute('class'):
            break  # Exit the loop if there's no next button or if it's disabled

        # Click the next button to load the next page of job listings
        next_button.click()
        logger.info("Clicked next button to load more jobs")
        time.sleep(3)
    except Exception as e:
        logger.error(f"Error during job data extraction: {e}")
        break

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "microsoft", "data": job_data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# print(job_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
