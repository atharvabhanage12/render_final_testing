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