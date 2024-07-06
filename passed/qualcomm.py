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
url = "https://qualcomm.wd5.myworkdayjobs.com/External?jobFamilyGroup=acda79515b8901afdab1c91926013304&jobFamilyGroup=acda79515b8901c2cf86ce1926013f04&jobFamilyGroup=acda79515b8901816a93ca1926013504&jobFamilyGroup=acda79515b8901046820cf1926014104"
driver.get(url)
L=[]
driver.implicitly_wait(20)
time.sleep(3)
num_str = driver.find_element(By.XPATH,"//p[@class='css-12psxof']").get_attribute("innerHTML")
ns = ""
for i in num_str:
    if i not in "0123456789":
        break
    else:
        ns+=i
int_num = int(ns)
count = 0
while len(L)<int_num:
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    total = soup.find_all("li",class_='css-1q2dra3')
    # print(len(total))
    # print(total)
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://qualcomm.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    total = soup.find_all("li",class_='css-3hlofn')
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://qualcomm.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    time.sleep(3)
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='css-jl3lyh' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        driver.quit()
        break
        

    
# json_data = json.dumps(L)
json_data = json.dumps({"company":"qualcomm","data":L})
# print(len(L))
driver.quit()
# print(int_num)
print(json_data)





