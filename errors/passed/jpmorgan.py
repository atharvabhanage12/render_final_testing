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
url = "https://careers.jpmorgan.com/in/en/students/programs?deeplink=multiTabNav1::tab2"
driver.get(url)
L=[]
driver.implicitly_wait(10)
element = driver.find_element(By.XPATH,"//a[@class='filter-menu-dropdown-click']")
driver.execute_script("arguments[0].click();", element)
time.sleep(3)
element = driver.find_element(By.XPATH,"//a[@data-filter-tag='Technology']")
driver.execute_script("arguments[0].click();", element)
time.sleep(3)
element = driver.find_element(By.XPATH,"//label[@for='aoi__Technology__Technology']")
driver.execute_script("arguments[0].click();", element)
time.sleep(3)

def continue_code(driver,classo,idx):
    global L
    ele = driver.find_elements(By.XPATH,"//p[@class='moduleTitle']")
    driver.execute_script("arguments[0].click();", ele[idx])
    time.sleep(4)
    current_html = driver.page_source
    soup = BeautifulSoup(current_html,"html.parser")
    job_elements = soup.find_all("div",class_='{}'.format(classo))
    driver.execute_script("window.scrollTo(0, 0.80*document.body.scrollHeight);")
    for i in job_elements:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("p",class_='type').text
        job_location = soup2.find("p",class_='location-name').text
        job_link = "https://careers.jpmorgan.com"+soup2.find("a",class_='event-name-href')["href"]
        job_description = soup2.find("p",class_='external-description').text.replace("\n"," ")
        L.append({"job_title":job_title,"job_description":job_description,"job_location":job_location,"job_link":job_link})
    driver.execute_script("window.scrollTo(0, 0.30*document.body.scrollHeight);")
    # print(len(job_elements))
continue_code(driver,"filter-display-card programs school active",0)
continue_code(driver,"filter-display-card programs preinternship active",1)
continue_code(driver,"filter-display-card programs internship active",2)
continue_code(driver,"filter-display-card programs fulltime active",3)
# print(len(L))
# json_data = json.dumps(L)
json_data = json.dumps({"company":"jpmorgan","data":L})
print(json_data)
driver.quit()

