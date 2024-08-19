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
chrome_options.add_argument("--headless")  # Uncomment if headless mode is needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path  # Set the Chrome binary location

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    logger.info("WebDriver initialized")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = 'https://careers.expediagroup.com/jobs/?filter[category]=Technology'
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

num_str = driver.find_element(By.XPATH, "//span[@id='totresultsspan']").get_attribute('innerHTML')
int_num = int(num_str)
logger.info(f"Total number of jobs: {int_num}")

L = []

def collect_job_details():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find_all("li", class_="Results__list__item")
    for job_element in job_elements:
        job_title = job_element.find("h3", class_='Results__list__title h4 text-blue-2').text.strip()
        job_link = job_element.find("a")["href"]
        if 'https' not in job_link:
            job_link = 'https://careers.expediagroup.com/jobs/' + job_link
        job_department = job_element.find("p").text.strip()
        job_location = job_element.find("h4", class_="Results__list__location h5").text.strip()
        L.append({"job_title": job_title, "job_link": job_link, "job_department": job_department, "job_location": job_location})

collect_job_details()
while True:
    try:
        load_more_button = driver.find_element(By.XPATH, "//button[@class='Results__button button button--blue-7']")
        driver.execute_script('arguments[0].click();', load_more_button)
        time.sleep(2)
        collect_job_details()
    except:
        logger.info("No more pages or an error occurred")
        break

    if len(L) >= int_num:
        logger.info("Collected all jobs")
        break

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "expedia", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON Expedia: {output_path}")

print(L)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
