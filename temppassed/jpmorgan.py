from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import json
import requests
from bs4 import BeautifulSoup
import time

firefox_options = Options()
firefox_options.binary_location = './firefox.exe'
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options,service=FirefoxService(GeckoDriverManager().install()))
url = "https://careers.jpmorgan.com/in/en/students/programs?deeplink=multiTabNav1::tab2"
driver.get(url)
L=[]
driver.implicitly_wait(10)
element = driver.find_element(By.XPATH,"//a[@class='filter-menu-dropdown-click']")
driver.execute_script("arguments[0].click();", element)
time.sleep(3)
element = driver.find_element(By.XPATH,"//a[@data-filter-tag='Technology']")
driver.execute_script("arguments[0].click();", element)
time.sleep(3)
element = driver.find_element(By.XPATH,"//label[@for='aoi__Technology__Technology']")
driver.execute_script("arguments[0].click();", element)
time.sleep(3)

def continue_code(driver,classo,idx):
    global L
    ele = driver.find_elements(By.XPATH,"//p[@class='moduleTitle']")
    driver.execute_script("arguments[0].click();", ele[idx])
    time.sleep(4)
    current_html = driver.page_source
    soup = BeautifulSoup(current_html,"html.parser")
    job_elements = soup.find_all("div",class_='{}'.format(classo))
    driver.execute_script("window.scrollTo(0, 0.80*document.body.scrollHeight);")
    for i in job_elements:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("p",class_='type').text
        job_location = soup2.find("p",class_='location-name').text
        job_link = "https://careers.jpmorgan.com"+soup2.find("a",class_='event-name-href')["href"]
        job_description = soup2.find("p",class_='external-description').text.replace("\n"," ")
        L.append({"job_title":job_title,"job_description":job_description,"job_location":job_location,"job_link":job_link})
    driver.execute_script("window.scrollTo(0, 0.30*document.body.scrollHeight);")
    # print(len(job_elements))
continue_code(driver,"filter-display-card programs school active",0)
continue_code(driver,"filter-display-card programs preinternship active",1)
continue_code(driver,"filter-display-card programs internship active",2)
continue_code(driver,"filter-display-card programs fulltime active",3)
# print(len(L))
# json_data = json.dumps(L)
json_data = json.dumps({"company":"jpmorgan","data":L})
print(json_data)
driver.quit()

