import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless if needed
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("starting")
# Path to the manually downloaded ChromeDriver
chrome_driver_path = os.path.expanduser("~/project/src/chromedriver/chromedriver")
print(f"ChromeDriver Path: {chrome_driver_path}")

# Ensure the ChromeDriver is executable
if not os.path.isfile(chrome_driver_path):
    raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")

os.chmod(chrome_driver_path, 0o755)  # Ensure it's executable

# Initialize WebDriver with exception handling
try:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
except Exception as e:
    print(f"Error initializing WebDriver: {e}")
    raise

print("driver")
# URL to scrape
url = "https://www.yahooinc.com/careers/search.html"
try:
    driver.get(url)
except Exception as e:
    print(f"Error accessing URL {url}: {e}")
    driver.quit()
    raise

print("hitting url")
driver.implicitly_wait(20)
time.sleep(3)
print("sleeping done")
L = []
soup = BeautifulSoup(driver.page_source, "html.parser")

print("beautiful soup")
# Expand the job categories
try:
    var0 = driver.find_element(By.XPATH, "//button[@data-target='#collapseJC']")
    driver.execute_script("arguments[0].click()", var0)
except Exception as e:
    print(f"Error expanding job categories: {e}")
    driver.quit()
    raise

time.sleep(2)

# Select specific job categories
job_categories = ["engineering", "softwaredevelopment", "design", "informationsystems", "internship", "research"]
for category in job_categories:
    try:
        checkbox = driver.find_element(By.ID, category)
        driver.execute_script("arguments[0].click()", checkbox)
    except Exception as e:
        print(f"Error selecting category {category}: {e}")

print("categories selected")

# Submit the job search form
try:
    submit = driver.find_element(By.XPATH, "//button[@id='search-page-find-jobs']")
    driver.execute_script("arguments[0].click()", submit)
except Exception as e:
    print(f"Error submitting search form: {e}")
    driver.quit()
    raise

time.sleep(3)

print("submit clicked")
# Load more results if available
previous_count = 0
while True:
    try:
        load_more = driver.find_element(By.XPATH, "//button[@class='btn my-3 loadMore']")
        driver.execute_script("arguments[0].click();", load_more)
        time.sleep(2)
        
        # Get the current number of job listings
        soup2 = BeautifulSoup(driver.page_source, "html.parser")
        total = soup2.find_all("tr", class_='jobTitle')
        current_count = len(total)
        
        # Check if the number of listings has increased
        if current_count == previous_count:
            break
        previous_count = current_count
    except Exception as e:
        # If the "Load More" button is not found, exit the loop
        print(f"Exiting loop: {e}")
        break

print("loading done")
# Parse the job listings
soup2 = BeautifulSoup(driver.page_source, "html.parser")
total = soup2.find_all("tr", class_='jobTitle')

print("parsing done")

# Extract job links
script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i < elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""
L1 = driver.execute_script(script)
hrefs = [i for i in L1 if "/careers/job/" in i]

# Collect job data
count = 0
for job in total:
    soup3 = BeautifulSoup(str(job), "html.parser")
    job_title = soup3.find("td", class_='col-6').text.strip()
    job_link = hrefs[count]
    job_location = soup3.find("div", class_="tableLocPrimary").text.strip()
    L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
    count += 1

print("data collected")
# Save the data as JSON
json_data = json.dumps({"company": "yahoo", "data": L}, indent=4)
print(json_data)

# Quit the driver
driver.quit()
