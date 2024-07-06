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
url = "https://careers.walmart.com/results?q=&page=1&sort=rank&jobCategory=00000161-7bad-da32-a37b-fbef5e390000,00000161-7bf4-da32-a37b-fbf7c59e0000,00000161-7bff-da32-a37b-fbffc8c10000,00000161-8bd0-d3dd-a1fd-bbd0febc0000,00000161-8be6-da32-a37b-cbe70c150000&jobSubCategory=0000015a-a577-de75-a9ff-bdff284e0000&expand=department,0000015e-b97d-d143-af5e-bd7da8ca0000,00000161-8be6-da32-a37b-cbe70c150000,brand,type,rate&type=jobs"
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)
num_str = driver.find_element(By.XPATH, "//span[@id='count_totalResults']").get_attribute('innerHTML')
int_num=int(num_str)


while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="search-result job-listing")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("a", class_='job-listing__link').text   
        job_link = soup2.find("a", class_="job-listing__link")["href"]
        job_department = soup2.find("span", class_="job-listing__department eyebrow").text
        job_location = soup2.find("span", class_="job-listing__location").text
        job_created_on = soup2.find("span", class_="job-listing__created").text
        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location, "job_created_on":job_created_on})
        # print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location, "job_created_on":job_created_on})
        # print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//button[@class='search__results__pagination__arrow' and @data-page='next']")
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

json_data=json.dumps({'company':'walmart','data':L})
print(json_data)
driver.quit()