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
#take the url of website
url = "https://www.meesho.io/jobs"
#this code gets the info from the url given
driver.get(url)
#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
#we can execute javascript code using driver.execute_script here i used javascript to scroll down to bottom
driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
#selecting the input box (filters selection box ) in website and clicking it
driver.find_element(By.XPATH,"//a[@id='rdts1_trigger']").click()
#waiting for some time to get the changes loaded
time.sleep(3)
#loading the filters we want to select
filters = ["Tech"]
# filters=["Product, Design & UR"]
final_data=[]
for i in filters:
    #selecting the required filters using regex expression
    driver.find_element(By.XPATH,"//label[@title='{}']".format(i)).click()
    #waiting for the changes to load
    time.sleep(3)
#clicking on meesho searchbar or anywhere to apply the filters
driver.find_element(By.XPATH,"//input[@role='combobox']").click()
#waiting for the changes to occur
time.sleep(3)
#getting the info of the html source code using beautiful soup and driver.page_source which gives the source code of html file
soup = BeautifulSoup(driver.page_source,"html.parser")
#finding all the job_positings divs
job_elements = soup.find_all("div",class_='job')
# print(len(job_elements))
for i in job_elements:
    #gettting info of all the job listings
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_link = url+soup2.find("a",attrs={"rel":"noreferrer"})["href"][5:]
    job_title = soup2.find("div",class_='col-span-5 py-4 text-md lg:text-lg text-dark lg:text-primary').text
    job_category = soup2.find("div",class_='col-span-4 py-4 text-sm lg:text-lg text-dark').text
    job_location = soup2.find("div",class_='flex').text
    final_data.append({"job_title":job_title,"job_category":job_category,"job_location":job_location,"job_link":job_link})
    # print(json.dumps({"job_title":job_title,"job_category":job_category,"job_location":job_location,"job_link":job_link}))
#in meesho website there is another switch for internships instead of jobs as we have to collect those also we eill click the button for internships
driver.find_element(By.XPATH,"//button[@id='headlessui-switch-3']").click()
#waiting for changes to occur
time.sleep(3)
#for interns
time.sleep(3)
soup = BeautifulSoup(driver.page_source,"html.parser")
job_elements = soup.find_all("div",class_='job')
# print(len(job_elements))
for i in job_elements:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_link = url+soup2.find("a",attrs={"rel":"noreferrer"})["href"][5:]
    job_title = soup2.find("div",class_='col-span-5 py-4 text-md lg:text-lg text-dark lg:text-primary').text
    job_category = soup2.find("div",class_='col-span-4 py-4 text-sm lg:text-lg text-dark').text
    job_location = soup2.find("div",class_='flex').text
    final_data.append({"job_title":job_title,"job_category":job_category,"job_location":job_location,"job_link":job_link})
    # print(json.dumps({"job_title":job_title,"job_category":job_category,"job_location":job_location,"job_link":job_link}))
#converting the data into json
json_data = json.dumps({"company":"meesho","data":final_data})
# json_data = json.dumps({"company":"meesho","data":final_data})
print(json_data)
#driver.quit()exits selenium
driver.quit()
