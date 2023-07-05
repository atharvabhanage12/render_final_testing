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
url = "https://bnymellon.eightfold.ai/careers?query=Technology&location=India&pid=13425925&domain=bnymellon.com&sort_by=relevance&triggerGoButton=false"
#this code gets the info from the url given
driver.get(url)
# driver.quit()
#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
s = BeautifulSoup(driver.page_source,"html.parser")
j = s.find_all("div",class_="position-title line-clamp line-clamp-2 line-clamp-done")
l = s.find_all("p",class_="position-location line-clamp line-clamp-2 body-text-2 p-up-margin line-clamp-done")
loc=[]
for i in l:
    st = i.text
    s = st[0:len(st)-10]
    loc.append(s)
data =[]
for i in range(len(j)):
    jobs={
        "job_title":j[i].text,
        "job_location":loc[i],
        "job_link":'https://bnymellon.eightfold.ai/careers',
    }
    data.append(jobs)
driver.quit()
json_data = json.dumps({"company":"bny","data":data})
print(json_data)