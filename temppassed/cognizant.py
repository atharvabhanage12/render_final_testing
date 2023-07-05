from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time
import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time
firefox_options = Options()
firefox_options.binary_location = './firefox.exe'
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options,service=FirefoxService(GeckoDriverManager().install()))
url ="https://careers.cognizant.com/global/en/c/technology-engineering-jobs?s=1"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
L = []

def function1():
    soup = BeautifulSoup(driver.page_source,"html.parser")
    job_elements = soup.find_all("li", class_ ='jobs-list-item')
    for i in job_elements:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("span", attrs={'data-ph-id':'ph-page-element-page2-28'}).text
        job_link = soup2.find("a", attrs={'data-ph-id':'ph-page-element-page2-24'})["href"]
        job_location = soup2.find("span", attrs={'data-ph-id':'ph-page-element-page2-31'}).text
        L.append({"job_title":job_title,"job_location":job_location,"job_link": job_link})
function1()
while True: 
    try:
        element = driver.find_element(By.XPATH, "//span[@data-ph-id='ph-page-element-page2-077i6t-077i6t-100']")
        driver.execute_script("arguments[0].click()", element)
        time.sleep(3)
        function1()
    except:
        break
json_data = json.dumps({"company":"cognizant","data":L})
print(json_data)
driver.quit()