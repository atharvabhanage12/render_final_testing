from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
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
url = "https://hiring.lenskart.com/"
driver.get(url)
L=[]
tech_ele = driver.find_element(By.XPATH,"//select[@id='department']")
driver.execute_script("arguments[0].click();", tech_ele)
sub_tech_ele = driver.find_element(By.XPATH,"//option[@value='Technology']")
driver.execute_script("arguments[0].click();", sub_tech_ele)
time.sleep(3)
current_html = driver.page_source
soup = BeautifulSoup(current_html,"html.parser")
tech_elem = soup.find_all("a",class_='job job__row')
for i in tech_elem:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_title = soup2.find("h5",class_='title').text.replace("\n","")
    job_location = soup2.find("span",class_='location').text.replace("\n","")
    job_link = "https://hiring.lenskart.com"+i["href"]
    L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
json_data = json.dumps({"company":"lenskart","data":L})
# json_data = json.dumps({"company":"lenskart","data":L})
print(json_data)
driver.quit()
