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
url = "https://codenation.org/careers/"
#this code gets the info from the url given
driver.get(url)

#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)

# driver.execute_script("arguments[0].click()",driver.find_element(By.XPATH,"//a[@class='cta cta--contained cta--icon cta--black cta--mobile-black']"))
# time.sleep(3)
soap = BeautifulSoup(driver.page_source,"html.parser")
# driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
# time.sleep(3)
j = str(soap.find_all("h2",class_="blog-shortcode-post-title entry-title fusion-responsive-typography-calculated"))
soap2 = BeautifulSoup(j,"html.parser")
jobs = soap2.find_all("a")

data =[]
for i in range(len(jobs)):
    s=jobs[i].text
    job = s[14:29]
    loc = s[32:]
    job_data ={
        "job_title":job,
        "job_location":loc,
        "job_link":jobs[i]["href"]
    }
    data.append(job_data)
   
# print(data)
json_data = json.dumps({"company":"codenation","data":data})
print(json_data)
driver.quit()