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
fin_data=[]
firefox_options = Options()
firefox_options.binary_location = './firefox.exe'
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options,service=FirefoxService(GeckoDriverManager().install()))
url = "https://www.flipkartcareers.com/#!/joblist"
driver.get(url)
L=[]
driver.implicitly_wait(10)
driver.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
ele = driver.find_element(By.XPATH,"//a[@class='closeOpenBtn cl-ck-btn']")
driver.execute_script("arguments[0].click();", ele)
time.sleep(2)
tech_ele = driver.find_element(By.XPATH,"//input[@id='Function_Technology']")
driver.execute_script("arguments[0].click();", tech_ele)
time.sleep(3)
current_html = driver.page_source
soup = BeautifulSoup(current_html,"html.parser")
num_elem = soup.find_all("p",class_='f-16 wow fadeInUp')
# print(num_elem)
numtxt =""
for i in num_elem:
    txt = i.text
    if "Openings" in txt:
        numtxt = txt


num_str=""
# print(numtxt)
for i in numtxt:
    if i not in "0123456789":
        if num_str!="":
            break
    else:
        num_str+=i
numb = int(num_str)
updated_html = driver.page_source
soup2 = BeautifulSoup(updated_html,"html.parser")
job_elems = soup2.find_all("div",class_='opening-block wow fadeInUp')
total = len(job_elems)
while total<numb:
    elem=driver.find_element(By.XPATH,"//button[@class='loadmore-btn']")
    driver.execute_script("arguments[0].click();", elem)
    time.sleep(2)
    updated_html = driver.page_source
    soup2 = BeautifulSoup(updated_html,"html.parser")
    job_elems = soup2.find_all("div",class_='opening-block wow fadeInUp')
    total = len(job_elems)
    # print(total)
job_elems = driver.find_elements(By.XPATH,"//div[@class='opening-block wow fadeInUp']")
count = 0
for i in job_elems:
    count+=1
    job_title = i.find_element(By.CLASS_NAME,"block-h").text
    job_location = i.find_element(By.CLASS_NAME,"wrap-long-text").text
    job_link = i.find_element(By.CLASS_NAME,"block-h")
    driver.execute_script("arguments[0].click();", job_link)
    time.sleep(1)
    window_handles = driver.window_handles
    main_original = window_handles[0]
    original_tab_handle = window_handles[-1]
    driver.switch_to.window(original_tab_handle)
    job_link = driver.current_url
    driver.close()

    # original_tab_handle = window_handles[0]
    driver.switch_to.window(main_original)
    fin_data.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
# json_data = json.dumps(fin_data)
json_data = json.dumps({"company":"flipkart","data":fin_data})
# json_data = json.dumps({"company":"flipkart","data":fin_data})
print(json_data)
driver.quit()

