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
url = "https://jobs.intuit.com/search-jobs/"
driver.get(url)
L=[]
driver.implicitly_wait(15)
# x = int(driver.find_element(By.XPATH,"//span[@class='pagination-total-pages']").text[2:])
element_filter = driver.find_element(By.XPATH,"//button[@id='category-toggle']")
element_filter.click()
initial_html = driver.page_source
soup = BeautifulSoup(initial_html,"html.parser")
filter_elements = soup.find_all("span",class_='filter__facet-name')
L1=[]
L2=[]
filters=["Data","Information Technology","Software Engineering"]
for i in filter_elements:
    if i.text in filters:
        L1.append(i)
for i in L1:
    L2.append(str(i.parent['for']))
for i in L2:
    time.sleep(3)
    driver.find_element(By.XPATH,"//label[@for='{}']".format(i)).click()
element_filter = driver.find_element(By.XPATH,"//button[@id='category-toggle']")
element_filter.click()
time.sleep(3)
x = int(driver.find_element(By.XPATH,"//span[@class='pagination-total-pages']").text[2:])
for i in range(x):
    time.sleep(4)
    updated_html = driver.page_source
    soup = BeautifulSoup(updated_html,"html.parser")
    job_elements = soup.find_all("a",class_='sr-item')
    for j in job_elements:
        soup2 = BeautifulSoup(str(j),"html.parser")
        job_title = soup2.find("h2").text
        job_location = soup2.find("span",class_='job-location').text
        job_link = url+str(soup2.find("a",class_='sr-item')["href"][1:])
        if {"job_title":job_title,"job_location":job_location,"job_link":job_link} not in L:
            L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # print(L[len(L)-1])
    if i!=x-1:
        try:
            driver.find_element(By.XPATH,"//a[@class='next']").click()
        except:
            driver.implicitly_wait(20)
            element = driver.find_element(By.XPATH,"//a[@class='next']")
            driver.execute_script("arguments[0].click();", element)
    driver.implicitly_wait(30)
json_data = json.dumps({"company":"intuit","data":L})
# json_data = json.dumps({"company":"intuit","data":L})
# print(len(L))
print(json_data)

driver.quit()
    

