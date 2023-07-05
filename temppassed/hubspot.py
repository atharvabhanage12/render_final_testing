#import webdriver
import os
# os.environ['PATH'] += r"C:/Users/ANUBHAB/Downloads/geckodriver-v0.33.0-win-aarch64"
from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.binary_location = './firefox.exe'
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
chrome_options.add_argument("--headless")
driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))
#take the url of website
url = "https://www.hubspot.com/careers/jobs?hubs_signup-url=www.hubspot.com%2Fcareers&hubs_signup-cta=careers-homepage-hero&page=1#department=product-ux-engineering;"
#this code gets the info from the url given
driver.get(url)

# driver.quit()
#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
s = BeautifulSoup(driver.page_source,"html.parser")
a = driver.find_element(By.PARTIAL_LINK_TEXT,'Show all')
a.click()
time.sleep(3)
soap = BeautifulSoup(driver.page_source,"html.parser")
jobs = soap.find_all("h3",class_="sc-htpNat jPYStQ")
locations = soap.find_all("p",class_="sc-ifAKCX gHfmgn")
links = soap.find_all("a",class_="sc-EHOje iHOrDr cta--primary cta--small careers-apply")
data =[]
for i in range(len(jobs)):
    job_data={
        "job_title":jobs[i].text,
        "job_location":locations[i].text,
        "job_link":"https://www.hubspot.com"+links[i]["href"]
    }
    data.append(job_data)

# json_data = json.dumps(data)
json_data = json.dumps({"company":"hubspot","data":data})
driver.quit()
print(json_data)

