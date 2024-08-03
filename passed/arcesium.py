# The webiste has changed"




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
# chrome_binary_path = "/driver/chrome-linux64/chrome"
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
url = "https://careers.arcesium.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=&optionsFacetsDD_dept=Technology"
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
count = 0

try:
    element = driver.find_element(By.XPATH, "//ul[@class='pagination']")
    elements = driver.find_elements(By.TAG_NAME, "a")
    L1 = []
    titles = []
    for i in elements:
        try:
            title = i.get_attribute("title")
            if "Page" in title:
                if title not in titles:
                    titles.append(title)
                    if title != "First Page" and title != "Last Page":
                        L1.append(i)
        except:
            pass
    elements = L1[1:]
    soup2 = BeautifulSoup(driver.page_source, "html.parser")
    elements1 = soup2.find_all("tr", class_="data-row")
    for j in elements1:
        soup3 = BeautifulSoup(str(j), "html.parser")
        job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
        job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
        job_link = "https://careers.arcesium.com/" + soup3.find("a", class_="jobTitle-link")["href"]
        if {"job_title": job_title, "job_location": job_location, "job_link": job_link} not in L:
            L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})

    for i in range(len(elements)):
        k = elements[i]
        driver.execute_script("arguments[0].click();", k)
        time.sleep(3)
        soup2 = BeautifulSoup(driver.page_source, "html.parser")
        elements1 = soup2.find_all("tr", class_="data-row")
        for j in elements1:
            soup3 = BeautifulSoup(str(j), "html.parser")
            job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
            job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
            job_link = "https://careers.arcesium.com/" + soup3.find("a", class_="jobTitle-link")["href"]
            if {"job_title": job_title, "job_location": job_location, "job_link": job_link} not in L:
                L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})

except Exception as e:
    logger.error(f"Error while extracting data: {e}")
    soup2 = BeautifulSoup(driver.page_source, "html.parser")
    elements = soup2.find_all("tr", class_="data-row")
    for i in elements:
        soup3 = BeautifulSoup(str(i), "html.parser")
        job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
        job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
        job_link = "https://careers.arcesium.com/" + soup3.find("a", class_="jobTitle-link")["href"]
        L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})

logger.info("Data collection complete")

# Save the data as JSON and log it
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "arcesium", "data": L}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Quit the driver
driver.quit()
logger.info("Driver quit, script completed")
