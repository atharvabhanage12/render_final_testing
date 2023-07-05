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


   
