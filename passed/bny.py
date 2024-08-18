###### . NOT SCRAPPING THE FILTERED DATA ALSO NOT SCRAPING THE ALL THE DATA AS WE NEED TO LOAD MORE###


import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json

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

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to the manually downloaded ChromeDriver
chrome_driver_path = os.path.expanduser("/opt/render/project/src/chrome/chrome-linux64/chrome")
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
url = "https://bnymellon.eightfold.ai/careers?location=India&department=Early%20Talent%20and%20University%20Programs&department=Tech%20-%20Architecture&department=Tech%20-%20Business%20Analysis&department=Tech%20-%20Data%20Management&department=Tech%20-%20Business%20Management&department=Tech%20-%20Information%20Security&department=Tech%20-%20Software%20Engineering&department=Tech%20-%20Tech%20Risk%2FCtrl%20%26%20Gov&department=Data%20and%20Quantitative%20Analysis&domain=bnymellon.com&sort_by=relevance&pid=21952323"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

# Wait until the page is loaded
driver.implicitly_wait(20)

# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
logger.info("Page source obtained and parsed with BeautifulSoup")

# Extract job titles and locations
job_titles = soup.find_all("div", class_="position-title line-clamp line-clamp-2")
job_locations = soup.find_all("p", class_="position-location line-clamp line-clamp-2 body-text-2 p-up-margin")

# Extract locations excluding <i> tags
locations = [loc.get_text(strip=True) for loc in job_locations]

# Extract titles text
titles = [title.get_text(strip=True) for title in job_titles]

data = []
for title, location in zip(titles, locations):
    job = {
        "job_title": title,
        "job_location": location,
        "job_link": 'https://bnymellon.eightfold.ai/careers',
    }
    data.append(job)

logger.info("Data collection complete")

# Save the data as JSON and log it

output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "bny", "data": data}, f, indent=4)
logger.info(f"Data saved to JSON BNY: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
