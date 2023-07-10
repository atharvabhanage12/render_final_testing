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
service = Service(ChromeDriverManager().install())
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
website = "https://www.janestreet.com/join-jane-street/open-roles/?type=students-and-new-grads&location=all-locations&department=technology"

# driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))

driver.get(website)

time.sleep(4)

soup = BeautifulSoup(driver.page_source, 'html.parser')

job_div = soup.find('div', class_='jobs-container row')

jobs = job_div.find_all('a')

job_data = []

for job in jobs:
    link = 'https://www.janestreet.com' + job['href']
    title = job.find('div', class_='item students-and-new-grads position').get_text()
    location = job.find('div', class_='item students-and-new-grads city').get_text()

    driver.get(link)

    about = driver.find_element(By.XPATH, '//div[@class="job-content row"]').text

    time.sleep(5)
    job_data.append({'job_title' : str(title), 'job_location' : str(location), 'job_link' : str(link), 'job_desc' : str(about)})

driver.quit()
print(json.dumps({"company":"jane_street","data":job_data}))