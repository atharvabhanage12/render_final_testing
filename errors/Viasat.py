#import webdriver
import os
from selenium import webdriver
import chromedriver_binary
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service 
#from webdriver_manager.firefox import GeckoDriverManager
#geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
service = Service(ChromeDriverManager().install())
firefox_options = Options()
#firefox_options.binary_location = os.environ["PATHCHROME"]
#firefox_options.binary_location = './firefox/firefox'
import os
#os.chmod('./firefox/firefox', 0o755)
# firefox_options.binary_location = geckodriver_path
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=firefox_options,service=service)
driver.maximize_window()

# Navigate to the website
driver.get("https://careers.viasat.com/jobs?limit=100&page=1")

# Wait for the job list to load

job_data = []

while True:
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-results-container")))

    # Get all the job elements
    job_elements = driver.find_elements(By.TAG_NAME, "mat-expansion-panel")

    # Iterate over the job elements and extract the job information
    for job_element in job_elements:
        # Extract job title
        title_element = job_element.find_element(By.CSS_SELECTOR, '.job-title')
        job_title = title_element.text.strip()

        # # Extract job location
        location_element = job_element.find_element(By.CSS_SELECTOR, ".label-container > span:nth-of-type(2)")
        job_location = location_element.text.strip()

        # Extract job description
        description_element = job_element.find_element(By.CSS_SELECTOR, ".job-result__categories > p span:nth-of-type(2)")
        job_description = description_element.text.strip()

        job_details = {
            'job_title': job_title,
            'job_location': job_location,
            'job_category': job_description,
            "job_link":'https://careers.viasat.com/'
        }


        # Append the job details to the job data list
        job_data.append(job_details)

    next_button = driver.find_element(By.CSS_SELECTOR, ".mat-paginator-range-actions > button:nth-of-type(2)")
    if "mat-button-disabled" in next_button.get_attribute('class'):
        break  # Exit the loop if there's no next button or if it's disabled

    # Click the next button to load the next page of job listings
    # next_button.click()
    driver.execute_script("arguments[0].click();", next_button)

    # Wait for the new page to load
    # wait.until(EC.staleness_of(job_elements[0]))

    # # Get the job elements of the new page
    # job_elements = driver.find_elements(By.CSS_SELECTOR, ".search-result job-listing   ")

# with open('Walmart.json', 'w') as file:
#     json.dump(job_data, file, indent=4)
print(json.dumps({"company":"viasat","data":job_data}))

# Close the browser
driver.quit()
