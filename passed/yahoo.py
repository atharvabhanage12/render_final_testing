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
import logging

# Configure logging to both console and file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('scraper.log'),
                        logging.StreamHandler()
                    ])

try:
    logging.info("Starting script...")

    # Define the path to the Chrome binary
    chrome_binary_path = "/opt/render/project/.render/chrome"
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = chrome_binary_path

    # Set up the Chrome service
    service = Service(executable_path=chrome_binary_path)

    # Initialize the WebDriver
    logging.info("Initializing WebDriver...")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://www.yahooinc.com/careers/search.html"
    logging.info(f"Navigating to {url}...")
    driver.get(url)
    driver.implicitly_wait(20)

    # Click the necessary buttons and select filters
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-target='#collapseJC']"))
    ).click()
    logging.info("Expanded job categories.")

    filter_ids = ["engineering", "softwaredevelopment", "desing", "informationsystems", "internship", "research"]
    for filter_id in filter_ids:
        checkbox = driver.find_element(By.ID, filter_id)
        if not checkbox.is_selected():
            checkbox.click()
    logging.info("Applied filters.")

    submit_button = driver.find_element(By.ID, "search-page-find-jobs")
    submit_button.click()
    logging.info("Submitted job search.")

    # Wait for results to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[@class='resultsTotal']"))
    )
    logging.info("Results loaded.")

    # Load more results if available
    while True:
        try:
            load_more_button = driver.find_element(By.XPATH, "//button[@class='btn my-3 loadMore']")
            load_more_button.click()
            time.sleep(2)
        except Exception as e:
            logging.info("No more 'Load More' button found.")
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
    logging.info("Job data collected.")
    print(json_data)

    driver.quit()

except Exception as e:
    logging.error("An error occurred", exc_info=True)
    driver.quit()
    print(f"Error: {str(e)}")
