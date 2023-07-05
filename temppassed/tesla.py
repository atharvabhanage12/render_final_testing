from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import json
import requests
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.binary_location = './firefox.exe'
chrome_options.add_argument('--headless')
driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))
url = 'https://www.tesla.com/careers/search/?region=5'
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)

category = ['Autopilot & Robotics', 'Engineering & Information Technology', 'Vehicle Software']

def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height
    
    #print('done')

scroll_down()
soup = BeautifulSoup(driver.page_source, "html.parser")
total = soup.find_all("tr", class_="tds-table-row")
total.pop(0)

for i in total:

    soup2 = BeautifulSoup(str(i), "html.parser")
    #print(soup2)
    datasoup = soup2.find_all("td")
    job_title = datasoup[0].text
    job_link='https://www.tesla.com/'+datasoup[0].find('a')["href"]
    job_department=datasoup[1].text
    job_location=datasoup[2].text
    if job_department not in category:
        continue
    L.append({"job_title":job_title, 'job_link':job_link, "job_department":job_department, "job_location":job_location})
    #print({"job_title":job_title, 'job_link':job_link, "job_department":job_department, "job_location":job_location})
    #print(len(L))

json_data=json.dumps({'company':'tesla','data':L})
print(json_data)
driver.quit()