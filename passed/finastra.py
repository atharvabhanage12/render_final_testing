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
url = 'https://careers.finastra.com/jobs'
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(20)
time.sleep(2)

num_str = driver.find_element(By.XPATH, "//h2[@id='search-results-indicator']").get_attribute('innerHTML')
num = ''.join(filter(str.isdigit, num_str))
int_num = int(num)
logger.info(f"Total number of jobs: {int_num}")

categories = [
    'Engineering Support Services', 'Development', 'Development Operations', 'Product Analysis', 'Information Security Governance',
    'Technical Client Support', 'Information Security', 'Audit and Business Controls', 'Quality Assurance Automation Engineering',
    'Release Engineering', 'Quality Assurance Engineering', 'Enterprise Application Support Development', 'Product Management', 'Intern/CoOp',
    'System Operations', 'Functional Implementation', 'Business Analysis', 'Digital Marketing', 'Database Management', 'Third Party Risk Management',
    'Client Support', 'Technical Project Management', 'Quality Control & IT Compliance','Network Operations', 'Technical Implementation',
    'Business Systems Analysis'
]

L = []

def collect_job_details():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_elements = soup.find_all("mat-expansion-panel-header")
    for job_element in job_elements:
        job_title = job_element.find("p", class_='job-title').text.strip()
        job_link = 'https://careers.finastra.com/' + job_element.find("a", class_="job-title-link")["href"]
        try:
            job_department = job_element.find("span", class_="label-value tags1").text.strip()
        except:
            job_department = 'Unknown'
        try:
            job_location = job_element.find("span", class_="label-value location").text.strip().replace('\n', ',').replace(',,', ',')
        except:
            job_location = 'Unknown'

        L.append({"job_title": job_title, "job_link": job_link, "job_department": job_department, "job_location": job_location})

collect_job_details()
while True:
    try:
        next_button_disabled = driver.find_element(By.XPATH, "//button[@aria-label='Next Page of Job Search Results']").get_attribute('disabled')
        if next_button_disabled == 'true':
            logger.info("No more pages to load")
            break

        next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next Page of Job Search Results"]')
        driver.execute_script('arguments[0].click();', next_button)
        time.sleep(2)
        collect_job_details()
    except Exception as e:
        logger.info(f"Pagination ended or an error occurred: {e}")
        break

    if len(L) >= int_num:
        logger.info("Collected all jobs")
        break

# Filter jobs based on categories and job titles
L = [job for job in L if job['job_department'] in categories or 'Engineer' in job['job_title']]

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "finastra", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON finashtra: {output_path}")

# Close the browser
driver.quit()
logger.info("Driver quit, script completed")
