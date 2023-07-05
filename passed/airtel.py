#import webdriver
import os
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path

firefox_options = Options()
firefox_options.binary_location = './firefox/firefox.exe'
import os
os.chmod('./firefox/firefox.exe', 0o755)
# firefox_options.binary_location = geckodriver_path
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)
#take the url of website
url = "https://eeji.fa.em3.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1/requisitions"
#this code gets the info from the url given
driver.get(url)
#this code is to wait till the data gets loaded from url
driver.implicitly_wait(10)
#we can execute javascript code using driver.execute_script here i used javascript to scroll down to bottom
for i in range(10):
    driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
    #waiting for some time to get the changes loaded
    time.sleep(3)
final_data=[]

#getting the info of the html source code using beautiful soup and driver.page_source which gives the source code of html file
soup = BeautifulSoup(driver.page_source,"html.parser")
#finding all the job_positings divs
field = soup.find("ul", class_="jobs-list__list")
# print(field)
job_elements = field.find_all("a", class_="job-list-item__link")
# print(len(job_elements))
for i in job_elements:
    #getting info of all the job listings
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_link = soup2.find("a")["href"] #[5:]
    job_title = soup2.find("span", class_="job-tile__title").text
    # job_category = soup2.find("div",class_='col-span-4 py-4 text-sm lg:text-lg text-dark').text
    job_location = soup2.find("div", class_="job-tile__subheader").find("span").find("span").text
    final_data.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})

# print(len(final_data))
# #converting the data into json
json_data = json.dumps({"company":"airtel","data":final_data})
print(json_data)
# #driver.quit()exits selenium
driver.quit()
