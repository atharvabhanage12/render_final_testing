#import webdriver
import os
from selenium import webdriver
import chromedriver_binary
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service 
#from webdriver_manager.firefox import GeckoDriverManager
#geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
service = Service("/opt/render/project/.render/chrome/opt/google/chrome")
firefox_options = Options()
#firefox_options.binary_location = os.environ["PATHCHROME"]
#firefox_options.binary_location = './firefox/firefox'
import os
#os.chmod('./firefox/firefox', 0o755)
# firefox_options.binary_location = geckodriver_path
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=firefox_options,service=service)
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