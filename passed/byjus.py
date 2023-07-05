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
url = "https://byjus.com/careers/all-openings/job-category/tech/"
#this code gets the info from the url given
driver.get(url)

#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
s = BeautifulSoup(driver.page_source,"html.parser")
sp = str(s.find_all("li",class_="left post-90886 job_listing type-job_listing status-publish hentry job_listing_category-tech job_listing_type-permanent job-type-permanent"))
j = BeautifulSoup(sp,"html.parser")
h1 = j.find_all("h4")[0].text
li = j.find("a")["href"]
time.sleep(3)
sp2 = str(s.find_all("li",class_="left post-90888 job_listing type-job_listing status-publish hentry job_listing_category-tech job_listing_type-permanent job-type-permanent"))
j2 = BeautifulSoup(sp2,"html.parser")
h2 = j.find_all("h4")[0].text
li2 = j.find("a")["href"]
jobs=[h1,h2]
links = [li,li2]

# loc = s.find_all("div",class_="css-1cm4lgc")
data =[]

for i in range(2):
    job_data ={
        "job_title":jobs[i],
        "job_link":links[i],
        "job_location":'unknown'
    }

    data.append(job_data)
driver.quit()
json_data = json.dumps({"company":"byjus","data":data})
print(json_data)