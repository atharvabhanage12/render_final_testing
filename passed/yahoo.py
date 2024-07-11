import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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

    # Define the path to the local Chromium binary
    # chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    # # Set up Chrome options
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.binary_location = chrome_binary_path

    # # Set up the Chrome service using webdriver-manager to manage chromedriver
    # chromium_version = '126.0.6478.127'  # Your Chrome version
    # service = Service(ChromeDriverManager(version=chromium_version).install(), options=chrome_options)

    # # Initialize the WebDriver
    # logging.info("Initializing WebDriver...")
    # driver = webdriver.Chrome(service=service)
    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    


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
    if 'driver' in locals():
        driver.quit()
    print(f"Error: {str(e)}")

# import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import time
# import json
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# import requests
# from bs4 import BeautifulSoup

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run headless if needed
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# # Set up ChromeDriver service
# service = Service(ChromeDriverManager().install())

# # Initialize WebDriver
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # URL to scrape
# url = "https://www.yahooinc.com/careers/search.html"
# driver.get(url)
# driver.implicitly_wait(20)
# time.sleep(3)

# L = []
# soup = BeautifulSoup(driver.page_source, "html.parser")

# # Expand the job categories
# var0 = driver.find_element(By.XPATH, "//button[@data-target='#collapseJC']")
# driver.execute_script("arguments[0].click()", var0)
# time.sleep(2)

# # Select specific job categories
# job_categories = ["engineering", "softwaredevelopment", "design", "informationsystems", "internship", "research"]
# for category in job_categories:
#     try:
#         checkbox = driver.find_element(By.ID, category)
#         driver.execute_script("arguments[0].click()", checkbox)
#     except Exception as e:
#         print(f"Error selecting category {category}: {e}")

# # Submit the job search form
# submit = driver.find_element(By.XPATH, "//button[@id='search-page-find-jobs']")
# driver.execute_script("arguments[0].click()", submit)
# time.sleep(3)

# # Load more results if available
# while True:
#     try:
#         load_more = driver.find_element(By.XPATH, "//button[@class='btn my-3 loadMore']")
#         driver.execute_script("arguments[0].click();", load_more)
#         time.sleep(2)
#     except:
#         break

# # Parse the job listings
# soup2 = BeautifulSoup(driver.page_source, "html.parser")
# total = soup2.find_all("tr", class_='jobTitle')

# # Extract job links
# script = """
#     var elements = document.querySelectorAll("a");
#     var href = [];
#     for (var i = 0 ; i < elements.length; i++){
#         href.push(elements[i].href);
#     }
#     return href;
# """
# L1 = driver.execute_script(script)
# hrefs = [i for i in L1 if "/careers/job/" in i]

# # Collect job data
# count = 0
# for job in total:
#     soup3 = BeautifulSoup(str(job), "html.parser")
#     job_title = soup3.find("td", class_='col-6').text.strip()
#     job_link = hrefs[count]
#     job_location = soup3.find("div", class_="tableLocPrimary").text.strip()
#     L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
#     count += 1

# # Save the data as JSON
# json_data = json.dumps({"company": "yahoo", "data": L}, indent=4)
# print(json_data)

# # Quit the driver
# driver.quit()
