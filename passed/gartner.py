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
chrome_options.binary_location = './firefox.exe'
chrome_options.add_argument("--headless")
driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))
url='https://jobs.gartner.com/jobs/?search=&department=Technology&contractType=&pagesize=20'
L = []
job_department = 'Technology'


driver.get(url)
driver.implicitly_wait(20)
time.sleep(2)
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("div", class_="card-body")
    #print(total)
    #print(len(total))

    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("a").text   
        job_link = 'https://jobs.gartner.com'+soup2.find("a")["href"]
        job_location = soup2.find("li",class_="list-inline-item").text.strip()
        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        # print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        # print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//a[@aria-label='Go to next page of results']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        #print("no button?")
        driver.quit()
        break

#print(len(L))

json_data=json.dumps({'company':'gartner','data':L})
print(json_data)
driver.quit()