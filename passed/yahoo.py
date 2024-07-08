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
url ="https://www.yahooinc.com/careers/search.html"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)
L = []
soup = BeautifulSoup(driver.page_source,"html.parser")
var0 = driver.find_element(By.XPATH,"//button[@data-target='#collapseJC']")
driver.execute_script("arguments[0].click()", var0)
time.sleep(2)
elem = driver.find_elements(By.XPATH,"//input[@class='custom-control-input']")
for i in elem: 
    var1 = i.get_attribute("id")
    if var1 == "engineering" or var1 == "softwaredevelopment" or var1=="desing" or var1=="informationsystems" or var1=="internship" or var1=="research" :
        driver.execute_script("arguments[0].click()", i)
        # time.sleep(2)
submit = driver.find_element(By.XPATH,"//button[@id='search-page-find-jobs']")
driver.execute_script("arguments[0].click()", submit)
time.sleep(3)
L =[]
while True:
    # soup = BeautifulSoup(driver.page_source,"html.parser")
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='btn my-3 loadMore']")
        # print(elem.get_attribute("outerHTML"))
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(2)
    except:
        break
    sentence = driver.find_element(By.XPATH,"//p[@class='resultsTotal']").text
    ns = ""
    for i in sentence:
        if i not in "0123456789":
            if ns!="":
                break
        else:
            ns+=i
    sn = ""
    i = len(sentence)-1
    while True:
        if sentence[i] in "0123456789":
            sn = sentence[i]+sn
            i-=1
        else:
            break
    if ns==sn:
        break
soup2 = BeautifulSoup(driver.page_source,"html.parser")
total = soup2.find_all("tr",class_='jobTitle')
#print(total)
script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i< elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""
L1 = driver.execute_script(script)
hrefs= []
for i in L1:
    if "/careers/job/" in i:
        hrefs.append(i)
count = 0
for i in total:
    soup3 = BeautifulSoup(str(i),"html.parser")
    job_title = soup3.find("td", class_ = 'col-6').text
    job_link =  hrefs[count]
    job_location = soup3.find("div",class_="tableLocPrimary").text
    L.append({"job_title":job_title,"job_location":job_location,"job_link": job_link})
    count+=1
json_data = json.dumps({"company":"yahoo","data":L})
print(json_data)
driver.quit()