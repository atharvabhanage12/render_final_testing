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

categories = ['Engineering Support Services', 'Development', 'Development Operations', 'Product Analysis', 'Information Security Governance',
              'Technical Client Support', 'Information Security', 'Audit and Business Controls', 'Quality Assurance Automation Engineering',
              'Release Engineering', 'Quality Assurance Engineering', 'Enterprise Application Support Development', 'Product Management', 'Intern/CoOp',
              'System Operations', 'Functional Implementation', 'Business Analysis', 'Digital Marketing', 'Database Management', 'Third Party Risk Management',
              'Client Support', 'Technical Project Management', 'Quality Control & IT Compliance','Network Operations', 'Technical Implementation',
              'Business Systems Analysis']


chrome_options = Options()
chrome_options.binary_location = './firefox.exe'
chrome_options.add_argument("--headless")
driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))
url='https://careers.finastra.com/jobs'
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)
num_str = driver.find_element(By.XPATH, "//h2[@id='search-results-indicator']").get_attribute('innerHTML')
num=''
for i in num_str:
    if i in '1234567890':
        num+=i
int_num=int(num)
#print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("mat-expansion-panel-header")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("p", class_='job-title').text   
        job_link = 'https://careers.finastra.com/' + soup2.find("a", class_="job-title-link")["href"]
        try:
            job_department = soup2.find("span", class_="label-value tags1").text
        except:
            job_department='Unknown'
        try:
            job_location = soup2.find("span", class_="label-value location").text.strip().replace('\n',',').replace(',,',',')
        except:
            job_location='Unknown'

        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        # print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        # print(len(L))
    try:
        exists = driver.find_element(By.XPATH,"//button[@aria-label='Next Page of Job Search Results']").get_attribute('disabled')
        # print(exists)
        # print(type(exists))
        if exists=='true':
            #print("done")
            driver.quit()
            break

        elem=driver.find_element(By.XPATH,'//button[@aria-label="Next Page of Job Search Results"]')
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

for i in L:
    if i['job_department'] not in categories and 'Engineer' not in i['job_title']:
        L.remove(i)

#print(len(L))

json_data=json.dumps({'company':'finastra','data':L})
print(json_data)
driver.quit()