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
        logging.FileHandler("workday_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting Workday scraping script")

# Set up Chrome options and ChromeDriver paths
chrome_binary_path = "/opt/render/project/src/chrome/chrome-linux64/chrome"
chrome_driver_path = os.path.expanduser("/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path

logger.info(f"ChromeDriver Path: {chrome_driver_path}")

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    logger.error(f"ChromeDriver not found at {chrome_driver_path}")
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)  # Ensure it's executable

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized for Workday")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://workday.wd5.myworkdayjobs.com/Workday?jobFamilyGroup=8c5ce7a1cffb43e0a819c249a49fcb00&jobFamilyGroup=a88cba90a00841e0b750341c541b9d56&jobFamilyGroup=4b2f970c50930155b9985193020a0c72"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

# Wait for the page to load
driver.implicitly_wait(100)
time.sleep(4)

# Get total number of job results
try:
    num_str = driver.find_element(By.XPATH, "//p[@class='css-12psxof']").get_attribute("innerHTML")
    ns = "".join([i for i in num_str if i.isdigit()])
    int_num = int(ns)
    logger.info(f"Total job listings found: {int_num}")
except Exception as e:
    logger.error(f"Error retrieving total job results: {e}")
    driver.quit()
    raise

# Initialize job list
L = []

# Function to parse and collect job data
def collect_job_data():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("li", class_="css-1q2dra3") + soup.find_all("li", class_="css-3hlofn")

    for card in job_cards:
        soup2 = BeautifulSoup(str(card), "html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://workday.wd5.myworkdayjobs.com" + soup2.find("a", class_="css-19uc56f")["href"]
        job_location = soup2.find("dd", class_="css-129m7dg").text
        L.append({
            "job_title": job_title,
            "job_location": job_location,
            "job_link": job_link
        })
        logger.info(f"Collected job: {job_title}, {job_location}")

# Loop to handle pagination and collect data
while True:
    collect_job_data()

    # Click the "Next" button to go to the next page, if available
    try:
        elem = driver.find_element(By.XPATH, "//button[@class='css-ly8o31' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
        logger.info("Moved to the next page")
    except Exception as e:
        logger.info("No more pages or encountered error moving to next page.")
        break

    if len(L) >= int_num:
        logger.info("Collected all job listings.")
        break

# Save the data as JSON and log it
output_path = "/opt/render/project/src/workday_jobs.json"
with open(output_path, "w") as outfile:
    json.dump({"company": "workday", "data": L}, outfile, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed for Workday")
