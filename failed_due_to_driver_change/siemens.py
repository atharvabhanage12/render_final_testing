from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import json
import requests
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))
L = []
url='https://jobs.siemens.com/careers?pid=563156115868726&organization=Technology&domain=siemens.com&sort_by=relevance&triggerGoButton=false'
driver.get(url)
driver.implicitly_wait(20)
time.sleep(2)

while True:
    try:
        elem=driver.find_element(By.XPATH,"//button[@class='btn btn-sm btn-secondary show-more-positions']")
        driver.execute_script('arguments[0].click();', elem)
        #print('next')
        time.sleep(2)
    except:
        #print("no button?")
        break
soup = BeautifulSoup(driver.page_source, "html.parser")
total = soup.find_all("div", class_="card position-card pointer")
# print(total)
# print(len(total))
#time.sleep(3)
for i in total:
    soup2 = BeautifulSoup(str(i), "html.parser")
    job_title = soup2.find("div", class_='position-title line-clamp line-clamp-2').text   
    job_department = soup2.find("div", class_="row").text
    job_location = soup2.find("p").text.strip()
    L.append({"job_title":job_title, "job_department":job_department, "job_location":job_location,"job_link":'https://jobs.siemens.com/careers'})
    # print({"job_title":job_title, "job_department":job_department, "job_location":job_location})
    # print(len(L))

# print(L)
# print(len(L))
# time.sleep(3)
for i in L:
        counter=0
        for j in L:
            if i == j:
                counter+=1
                if counter > 1:
                    L.remove(j)
# print(len(L))
# print(L)
json_data=json.dumps({'company':'siemens','data':L})
print(json_data)
driver.quit()