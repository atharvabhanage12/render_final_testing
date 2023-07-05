from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import requests
from bs4 import BeautifulSoup
import time
geckodriver_path = './Mozilla Firefox'
# webdriver.gecko.driver = geckodriver_path

firefox_options = Options()
firefox_options.binary_location = './firefox/firefox'
import os
os.chmod('./firefox/firefox', 0o755)
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options,service=FirefoxService(GeckoDriverManager().install()))
url = "https://careers.arcesium.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_country=&optionsFacetsDD_dept=Technology"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
L = []
count = 0
try:
    element = driver.find_element(By.XPATH, "//ul[@class='pagination']")
    elements = driver.find_elements(By.TAG_NAME, "a")
    L1=[]
    titles=[]
    for i in elements:
        try:
            title = i.get_attribute("title")
            # soup4 = BeautifulSoup(str(title), "html.parser")
            # title = soup4.find("a")["title"]
            
            if "Page" in title:
                if title not in titles:
                    titles.append(title)
                    if title!="First Page" and title!="Last Page":
                        L1.append(i)
                        # print(title)
        except:
            pass
    elements = L1[1:]
    soup2 = BeautifulSoup(driver.page_source,"html.parser")
    elements1 = soup2.find_all("tr", class_ = "data-row")
    for j in elements1:
        soup3 = BeautifulSoup(str(j),"html.parser")
        job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
        job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
        job_link = "https://careers.arcesium.com/"+ soup3.find("a", class_="jobTitle-link")["href"]
        if {"job_title":job_title,"job_location":job_location,"job_link":job_link} not in L:
            L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        
    for i in range(len(elements)):
        if True:
            k = elements[i]
            driver.execute_script("arguments[0].click();", k)
            time.sleep(3)
            soup2 = BeautifulSoup(driver.page_source,"html.parser")
            elements1 = soup2.find_all("tr", class_ = "data-row")
            for j in elements1:
                soup3 = BeautifulSoup(str(j),"html.parser")
                job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
                job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
                job_link = "https://careers.arcesium.com/"+ soup3.find("a", class_="jobTitle-link")["href"]
                if {"job_title":job_title,"job_location":job_location,"job_link":job_link} not in L:
                    L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
            

except: 
    soup2 = BeautifulSoup(driver.page_source,"html.parser")
    elements = soup2.find_all("tr", class_ = "data-row")
    for i in elements:
        soup3 = BeautifulSoup(str(i),"html.parser")
        job_title = soup3.find("a", class_="jobTitle-link").text.replace("\n", "")
        job_location = soup3.find("span", class_="jobLocation").text.replace("\n", "")
        job_link = "https://careers.arcesium.com/"+ soup3.find("a", class_="jobTitle-link")["href"]
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        
json_data = json.dumps({"company":"arcesium","data":L})
print(json_data)
driver.quit()
