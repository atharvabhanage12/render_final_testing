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
        logging.FileHandler("walmart_scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting Walmart scraping script")

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
    logger.info("WebDriver initialized for Walmart")
except Exception as e:
    logger.error(f"Error initializing WebDriver: {e}")
    raise

# URL to scrape
url = "https://careers.walmart.com/results?q=&page=1&sort=rank&jobCategory=00000161-7bad-da32-a37b-fbef5e390000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000015a-a577-de75-a9ff-bdff284e0000&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,00000161-8be6-da32-a37b-cbe70c150000,brand,type,rate&type=jobs"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

# Wait for the page to load
driver.implicitly_wait(20)
time.sleep(2)

# Get total number of job results
try:
    num_str = driver.find_element(By.XPATH, "//span[@id='count_totalResults']").get_attribute('innerHTML')
    int_num = int(num_str)
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
    total = soup.find_all("li", class_="search-result job-listing")
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("a", class_='job-listing__link').text   
        job_link = soup2.find("a", class_="job-listing__link")["href"]
        job_department = soup2.find("span", class_="job-listing__department eyebrow").text
        job_location = soup2.find("span", class_="job-listing__location").text
        job_created_on = soup2.find("span", class_="job-listing__created").text
        L.append({
            "job_title": job_title, 
            "job_link": job_link, 
            "job_department": job_department, 
            "job_location": job_location, 
            "job_created_on": job_created_on
        })
        logger.info(f"Collected job: {job_title}, {job_location}")

# Loop to handle pagination and collect data
while True:
    collect_job_data()

    # Click the "Next" button to go to the next page, if available
    try:
        elem = driver.find_element(By.XPATH, "//button[@class='search__results__pagination__arrow' and @data-page='next']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
        logger.info("Moved to the next page")
    except Exception as e:
        logger.info("No more pages or encountered error moving to next page.")
        break

    if len(L) >= int_num:
        logger.info("Collected all job listings.")
        break

# Save the data as JSON and log it
output_path = "/opt/render/project/src/walmart_jobs.json"
with open(output_path, "w") as outfile:
    json.dump({'company': 'walmart', 'data': L}, outfile, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed for Walmart")
