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
url ="https://jobs.cisco.com/jobs/SearchJobs/?21181=%5B186%2C194%2C187%2C191%2C202%2C185%2C55816092%5D&21181_format=6023&listFilterMode=1"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i< elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""
driver.find_element(By.XPATH,"//button[@class='onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button ot-close-icon']").click()
time.sleep(2)
L = []
def function1():
    L1 = driver.execute_script(script)
    hrefs= []
    for i in L1:
        if "/ProjectDetail/" in i:
            hrefs.append(i)
    count = 0
    element = driver.find_element(By.TAG_NAME,"tbody")
    soup = BeautifulSoup(str(element.get_attribute("outerHTML")), "html.parser")
    job_elements = soup.find_all("tr")
    for i in job_elements:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("td",attrs={"data-th":"Job Title"}).text
        job_link =  hrefs[count]
        job_location = soup2.find("td",attrs={"data-th":"Location"}).text
        if {"job_title":job_title,"job_location":job_location,"job_link": job_link} not in L:
            L.append({"job_title":job_title,"job_location":job_location,"job_link": job_link})
        count+=1
while True:
    driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
    try:
        element1 = driver.find_elements(By.XPATH, "//a[@class='pagination_item']")
        time.sleep(2)
        function1()
        next =[]
        for i in element1:
            var1 = i.text
            if ">>" in var1:
                next.append(i)
        if len(next) == 0:
            break
        else:
            driver.execute_script("arguments[0].click()", next[0])
            time.sleep(3)
    except:
        pass

json_data = json.dumps({"company":"cisco","data":L})
print(json_data)

driver.quit()