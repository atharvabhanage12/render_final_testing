import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import json

# Define the path to the Chrome binary
chrome_binary_path = "/opt/render/project/.render/chrome/opt/google/chrome/chrome"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = chrome_binary_path

# Set up the Chrome service
service = Service(executable_path=chrome_binary_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.yahooinc.com/careers/search.html"
driver.get(url)
driver.implicitly_wait(20)

# Click the necessary buttons and select filters
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-target='#collapseJC']"))
).click()

filter_ids = ["engineering", "softwaredevelopment", "desing", "informationsystems", "internship", "research"]
for filter_id in filter_ids:
    checkbox = driver.find_element(By.ID, filter_id)
    if not checkbox.is_selected():
        checkbox.click()

submit_button = driver.find_element(By.ID, "search-page-find-jobs")
submit_button.click()

# Wait for results to load
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//p[@class='resultsTotal']"))
)

# Load more results if available
while True:
    try:
        load_more_button = driver.find_element(By.XPATH, "//button[@class='btn my-3 loadMore']")
        load_more_button.click()
        time.sleep(2)
    except Exception:
        break

# Parse the job listings
soup = BeautifulSoup(driver.page_source, "html.parser")
job_rows = soup.find_all("tr", class_='jobTitle')

jobs = []
for job_row in job_rows:
    title = job_row.find("td", class_='col-6').text.strip()
    location = job_row.find("div", class_="tableLocPrimary").text.strip()
    link = job_row.find("a")['href']
    jobs.append({"job_title": title, "job_location": location, "job_link": link})

json_data = json.dumps({"company": "yahoo", "data": jobs}, indent=4)
print(json_data)

driver.quit()
