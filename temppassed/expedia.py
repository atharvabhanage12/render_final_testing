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
url = 'https://careers.expediagroup.com/jobs/?filter[category]=Technology'
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)
num_str = driver.find_element(By.XPATH, "//span[@id='totresultsspan']").get_attribute('innerHTML')
int_num=int(num_str)
#print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="Results__list__item")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("h3", class_='Results__list__title text-md').text   
        job_link = soup2.find("a")["href"]
        if 'https' not in job_link:
            job_link='https://careers.expediagroup.com/jobs/'+job_link
        job_department = soup2.find("p", class_="Results__list__team text-body").text
        job_location = soup2.find("p", class_="Results__list__location text-body").text.strip()
        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        #print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        #print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//button[@class='Results__button button button--blue-7']")
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

json_data=json.dumps({'company':'expedia','data':L})
print(json_data)
driver.quit()