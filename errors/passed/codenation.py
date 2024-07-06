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
service = Service("/opt/render/project/.render/chrome/opt/google/chrome")
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