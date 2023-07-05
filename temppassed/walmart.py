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
url = "https://careers.walmart.com/results?q=&page=1&sort=rank&jobCategory=00000161-7bad-da32-a37b-fbef5e390000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000015a-a577-de75-a9ff-bdff284e0000&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,00000161-8be6-da32-a37b-cbe70c150000,brand,type,rate&type=jobs"
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)
num_str = driver.find_element(By.XPATH, "//span[@id='count_totalResults']").get_attribute('innerHTML')
int_num=int(num_str)


while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="search-result job-listing")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("a", class_='job-listing__link').text   
        job_link = soup2.find("a", class_="job-listing__link")["href"]
        job_department = soup2.find("span", class_="job-listing__department eyebrow").text
        job_location = soup2.find("span", class_="job-listing__location").text
        job_created_on = soup2.find("span", class_="job-listing__created").text
        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location, "job_created_on":job_created_on})
        # print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location, "job_created_on":job_created_on})
        # print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//button[@class='search__results__pagination__arrow' and @data-page='next']")
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

json_data=json.dumps({'company':'walmart','data':L})
print(json_data)
driver.quit()