######## ERROR WEBSITE CHANGED ""
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
# chrome_options.add_argument("--headless")  # Run headless if needed
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
url = "https://careers.qualcomm.com/careers?department=CPU%20Engineering&department=Cyber%20Security%20Engineering&department=Data%20Analyst&department=Database%20Administration&department=Demand%20Analysis&department=Engineering%20Intern&department=Engineering%20Technician&department=Enterprise%20Architecture&department=Field%20Applications%20Engineering%20-%20ACIP&department=GPU%20ASICS%20Engineering&department=Hardware%20Applications%20Engineering&department=Hardware%20Engineering&department=Hardware%20Systems%20Engineering&department=IT%20Data%20Scientist&department=IT%20Networking&department=IT%20Management&department=IT%20Internal%20Audit&department=IT%20Engineering&department=IT%20Architect&department=IT%20Cloud%20Architect&department=IT%20Data%20Engineer&department=IP%20Operations&pid=446697500841&domain=qualcomm.com&sort_by=relevance"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(3)

# Extract the total number of job postings
try:
    num_str = driver.find_element(By.XPATH, "//p[@class='css-12psxof']").get_attribute("innerHTML")
    ns = "".join(filter(str.isdigit, num_str))
    int_num = int(ns)
    logger.info(f"Total number of jobs: {int_num}")
except Exception as e:
    logger.error(f"Error extracting number of jobs: {e}")
    driver.quit()
    raise

L = []

# Function to scrape job data from the current page
def scrape_jobs():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find_all("li", class_='css-1q2dra3') + soup.find_all("li", class_='css-3hlofn')
    hrefs = ["https://qualcomm.wd5.myworkdayjobs.com" + job.find("a", class_='css-19uc56f')["href"] for job in job_elements]
    
    for i, job in enumerate(job_elements):
        soup2 = BeautifulSoup(str(job), "html.parser")
        job_title = soup2.find("h3").text.strip()
        job_link = hrefs[i]
        job_location = soup2.find("dd", class_='css-129m7dg').text.strip()
        L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
        logger.info(f"Collected job: {job_title} in {job_location}")

# Scrape jobs until all job postings are collected
while len(L) < int_num:
    scrape_jobs()
    try:
        next_button = driver.find_element(By.XPATH, "//button[@class='css-jl3lyh' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", next_button)
        logger.info("Clicked next page button")
        time.sleep(3)
    except Exception as e:
        logger.info(f"No more pages to load or error encountered: {e}")
        break

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
# with open(output_path, "w") as f:
#     json.dump({"company": "qualcomm", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

print(L)
# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
