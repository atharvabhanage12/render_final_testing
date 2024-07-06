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
url ="https://careers.cognizant.com/global/en/c/technology-engineering-jobs?s=1"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
L = []

def function1():
    soup = BeautifulSoup(driver.page_source,"html.parser")
    job_elements = soup.find_all("li", class_ ='jobs-list-item')
    for i in job_elements:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("span", attrs={'data-ph-id':'ph-page-element-page2-28'}).text
        job_link = soup2.find("a", attrs={'data-ph-id':'ph-page-element-page2-24'})["href"]
        job_location = soup2.find("span", attrs={'data-ph-id':'ph-page-element-page2-31'}).text
        L.append({"job_title":job_title,"job_location":job_location,"job_link": job_link})
function1()
while True: 
    try:
        element = driver.find_element(By.XPATH, "//span[@data-ph-id='ph-page-element-page2-077i6t-077i6t-100']")
        driver.execute_script("arguments[0].click()", element)
        time.sleep(3)
        function1()
    except:
        break
json_data = json.dumps({"company":"cognizant","data":L})
print(json_data)
driver.quit()