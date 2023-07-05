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
    

