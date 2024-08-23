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
url = "https://www.flipkartcareers.com/#!/joblist"
try:
    driver.get(url)
    logger.info(f"Accessed URL: {url}")
except Exception as e:
    logger.error(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

driver.implicitly_wait(10)
time.sleep(2)

# Close the initial pop-up and select the Technology filter
driver.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
try:
    close_button = driver.find_element(By.XPATH, "//a[@class='closeOpenBtn cl-ck-btn']")
    driver.execute_script("arguments[0].click();", close_button)
    logger.info("Closed initial pop-up")
except Exception as e:
    logger.info(f"No pop-up to close: {e}")

time.sleep(2)

try:
    tech_filter = driver.find_element(By.XPATH, "//input[@id='Function_Technology']")
    driver.execute_script("arguments[0].click();", tech_filter)
    logger.info("Selected Technology filter")
except Exception as e:
    logger.error(f"Error selecting Technology filter: {e}")
    driver.quit()
    raise

time.sleep(3)

# Get the total number of job openings
current_html = driver.page_source
soup = BeautifulSoup(current_html, "html.parser")
num_elem = soup.find_all("p", class_='f-16 wow fadeInUp')
numtxt = ""
for i in num_elem:
    txt = i.text
    if "Openings" in txt:
        numtxt = txt

num_str = ""
for i in numtxt:
    if i not in "0123456789":
        if num_str != "":
            break
    else:
        num_str += i
numb = int(num_str)
logger.info(f"Total number of openings: {numb}")

# Scroll and load all job listings
fin_data = []
while True:
    updated_html = driver.page_source
    soup2 = BeautifulSoup(updated_html, "html.parser")
    job_elems = soup2.find_all("div", class_='opening-block wow fadeInUp')
    total = len(job_elems)
    if total >= numb:
        break
    try:
        load_more_button = driver.find_element(By.XPATH, "//button[@class='loadmore-btn']")
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(2)
    except Exception as e:
        logger.info(f"No more pages to load or an error occurred: {e}")
        break

job_elems = driver.find_elements(By.XPATH, "//div[@class='opening-block wow fadeInUp']")
for i in job_elems:
    job_title = i.find_element(By.CLASS_NAME, "block-h").text
    job_location = i.find_element(By.CLASS_NAME, "wrap-long-text").text
    job_link_elem = i.find_element(By.CLASS_NAME, "block-h")
    driver.execute_script("arguments[0].click();", job_link_elem)
    time.sleep(1)
    window_handles = driver.window_handles
    main_original = window_handles[0]
    original_tab_handle = window_handles[-1]
    driver.switch_to.window(original_tab_handle)
    job_link = driver.current_url
    driver.close()
    driver.switch_to.window(main_original)
    fin_data.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "flipkart", "data": fin_data}, f, indent=4)
logger.info(f"Data saved to JSON: {output_path}")

# Close the browser
driver.quit()
logger.info("Driver quit, script completed")
