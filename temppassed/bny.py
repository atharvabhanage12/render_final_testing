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