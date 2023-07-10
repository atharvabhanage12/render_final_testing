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
url = "https://www.pinterestcareers.com/job-search-results/?primary_category=Engineering"
#this code gets the info from the url given
driver.get(url)

#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
s = BeautifulSoup(driver.page_source,"html.parser")
c=0
job_list=[]
link_list=[]
# driver.quit()
# c=0
for i in range(30):
    
    st = "job-result"+str(c)
    jobs = s.find("a",id=st).text
    link = "https://www.pinterestcareers.com"+s.find("a",id=st)["href"]
    job_list.append(jobs)
    link_list.append(link)
    c+=1

elem = driver.find_element(By.XPATH,"//a[@id='pagination2']")
driver.execute_script("arguments[0].click();",elem)
s2 = BeautifulSoup(driver.page_source,"html.parser")
c=0
for i in range(27):
    
    st = "job-result"+str(c)
    jobs = s.find("a",id=st).text
    link = "https://www.pinterestcareers.com"+s.find("a",id=st)["href"]
    job_list.append(jobs)
    link_list.append(link)
    c+=1
data =[]
for i in range(len(job_list)):
    job_data={
        "job_title":job_list[i],
        "job_link":link_list[i],
        "job_location":'unknown'
    }
    data.append(job_data)
    
# json_data = json.dumps(data)
json_data = json.dumps({"company":"pinterest","data":data})
print(json_data)
driver.quit()


   
