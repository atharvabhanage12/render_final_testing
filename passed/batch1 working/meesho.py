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
# chrome_options.binary_location = chrome_binary_path

# Path to the manually downloaded ChromeDriver
chrome_driver_path = os.path.expanduser("driver/chromedriver-mac-arm64/chromedriver")
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
url = "https://www.meesho.io/jobs"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
time.sleep(3)

# Scroll down to load more jobs
driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")

# Select filters and apply them
try:
    driver.find_element(By.XPATH, "//a[@id='rdts1_trigger']").click()
    logger.info("Clicked on filter selection box")
    time.sleep(3)
    
    filters = ["Tech"]
    for i in filters:
        driver.find_element(By.XPATH, f"//label[@title='{i}']").click()
        logger.info(f"Selected filter: {i}")
        time.sleep(3)
    
    driver.find_element(By.XPATH, "//input[@role='combobox']").click()
    logger.info("Applied filters")
    time.sleep(3)
except Exception as e:
    logger.error(f"Error applying filters: {e}")
    driver.quit()
    raise

# Parse the job listings
final_data = []
soup = BeautifulSoup(driver.page_source, "html.parser")
job_elements = soup.find_all("div", class_='job')

for i in job_elements:
    soup2 = BeautifulSoup(str(i), "html.parser")
    job_link = url + soup2.find("a", attrs={"rel": "noreferrer"})["href"][5:]
    job_title = soup2.find("div", class_='col-span-5 py-4 text-md lg:text-lg text-dark lg:text-primary').text
    job_category = soup2.find("div", class_='col-span-4 py-4 text-sm lg:text-lg text-dark').text
    job_location = soup2.find("div", class_='flex').text
    final_data.append({"job_title": job_title, "job_category": job_category, "job_location": job_location, "job_link": job_link})
    logger.info(f"Collected job: {job_title} in {job_location}")

# # Switch to internships and collect data
# try:
#     driver.find_element(By.XPATH, "//button[@id='headlessui-switch-3']").click()
#     logger.info("Switched to internships")
#     time.sleep(3)
    
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     job_elements = soup.find_all("div", class_='job')
    
#     for i in job_elements:
#         soup2 = BeautifulSoup(str(i), "html.parser")
#         job_link = url + soup2.find("a", attrs={"rel": "noreferrer"})["href"][5:]
#         job_title = soup2.find("div", class_='col-span-5 py-4 text-md lg:text-lg text-dark lg:text-primary').text
#         job_category = soup2.find("div", class_='col-span-4 py-4 text-sm lg:text-lg text-dark').text
#         job_location = soup2.find("div", class_='flex').text
#         final_data.append({"job_title": job_title, "job_category": job_category, "job_location": job_location, "job_link": job_link})
#         logger.info(f"Collected internship: {job_title} in {job_location}")
# except Exception as e:
#     logger.error(f"Error collecting internship data: {e}")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "meesho", "data": final_data}, f, indent=4)
# logger.info(f"Data saved to JSON: {output_path}")

print(final_data)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
