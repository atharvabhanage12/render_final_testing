from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time
import csv
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
from selenium.webdriver.common.keys import Keys

firefox_options = Options()
firefox_options.binary_location = './firefox.exe'
firefox_options.add_argument("--headless")
# Set up Selenium webdriver
driver = webdriver.Firefox(options=firefox_options,service=FirefoxService(GeckoDriverManager().install()))

# Navigate to the Dell careers website
driver.get("https://careers.jio.com/frmfttxjobs.aspx?func=w+cpdiT6wL4=&loc=/wASbQn4xyQ=&expreq=/wASbQn4xyQ=&flag=ODA1dRYKXFY=")

driver.implicitly_wait(10)
#we can execute javascript code using driver.execute_script here i used javascript to scroll down to bottom
driver.execute_script("window.scrollTo(0,0.95*document.body.scrollHeight);")
time.sleep(3)

# Scrape all job listings from each page
final_data = []
# ns = ''
# while ns == "":
#     num_str = driver.find_element(By.XPATH, "//h1[@class='search-results-heading']").get_attribute("innerHTML")
#     for i in num_str:
#         if i not in "0123456789":
#             break
#         else:
#             ns += i
#     try:
#         int_num = int(ns)
#     except:
#         pass
# count = 0

while True:
    # Get the page source using Selenium
    page_source = driver.page_source
    
    # Create BeautifulSoup object
    soup = BeautifulSoup(page_source, "html.parser")
    # container = soup.find("section", id="search-results-list")
    total = soup.find_all("figure", class_="jobPointList")
    # print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        time.sleep(2)
        job_title = soup2.find("span").text
        job_link = "https://careers.jio.com/frmfttxjobs.aspx?func=w+cpdiT6wL4%3d&loc=%2fwASbQn4xyQ%3d&expreq=%2fwASbQn4xyQ%3d&flag=ODA1dRYKXFY%3d"
        job_location = ' '.join(soup2.find("p").find("span").text) #.split(',')[1:]
        final_data.append({"job_title":job_title, "job_location": job_location,"job_link":job_link})
        # print({"job_title":job_title, "job_location": job_location, "job_link":job_link})
    # break
    time.sleep(3)  
    try:
        # container = soup2.find("span", id="MainContent_lstJoblist_DataPager1")
        check_page = soup.find("span", id="MainContent_lstJoblist_DataPager1_ctl00_CurrentPageLabel").text.split()
        # print(check_page)
        if check_page[1] == check_page[3]:
            break
        elem = driver.find_element(By.XPATH,"//input[@name='ctl00$MainContent$lstJoblist$DataPager1$ctl00$lnkNext']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep (3)
            # print(type(elem))
    except:
        break  

# # Print the job listings
# for job in final_data:
#     print("Title:", job["title"])
#     print("Location:", job["location"])
#     print("Link:", job["link"])
#     print("--------------------")

json_data = json.dumps({"company":"jio","data":final_data})
print(json_data)

# print(len(final_data))

# # Close the Selenium webdriver
driver.quit()