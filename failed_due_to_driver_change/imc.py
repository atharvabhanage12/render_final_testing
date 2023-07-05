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
url = "https://careers.imc.com/in/en/search-results"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(2)
L = []

cookies=driver.find_element(By.XPATH,"//button[@class='btn primary-button au-target' and @click.delegate='acceptAndClose()']")
driver.execute_script('arguments[0].click();', cookies)

time.sleep(2)

category=driver.find_element(By.XPATH,"//input[@type='checkbox' and @data-ph-at-text='Technology']")
driver.execute_script('arguments[0].click();', category)

time.sleep(2)
num_str = driver.find_element(By.XPATH, "//span[@class='result-count']").get_attribute('innerHTML')
int_num=int(num_str)

#print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="jobs-list-item")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find(attrs={'data-ph-id' : "ph-default-1544535895472-ph-search-results-v2073sfp-q7xTkZ"}).text   
        job_link = soup2.find("a", class_="au-target")["href"]
        job_requirements = soup2.find(attrs={'data-ph-id': "ph-default-1544535895472-ph-search-results-v2073sfp-bPhXdP"}).text.strip()
        job_location = soup2.find("span", class_="job-location").text.strip()[11:]
        job_commitment = soup2.find("span", class_="au-target type").text.strip()
        L.append({"job_title":job_title, "job_link": job_link, "job_requirements": job_requirements, "job_location":job_location, "job_commitment":job_commitment})
        #print({"job_title":job_title, "job_link": job_link, "job_requirements": job_requirements, "job_location":job_location, "job_commitment":job_commitment})
        #print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//a[@aria-label='View next page']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        #print("no button?")
        driver.quit()
        break

    if len(L)>=int_num:
        #print('done')
        driver.quit()
        break

#print(len(L))

json_data=json.dumps({'company':'imc trading','data':L})
driver.quit()
print(json_data)
