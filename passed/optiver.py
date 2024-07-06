# from selenium import webdriver
# from selenium.webdriver.common.by import By
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
from selenium.webdriver.support.select import Select
# import time
# import json
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
# chrome_options = Options()
# chrome_options.binary_location = './firefox.exe'
website = "https://optiver.com/working-at-optiver/career-opportunities"
# chrome_options.add_argument("--headless")
# driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))

driver.get(website)

time.sleep(3)

select_element = driver.find_element(by=By.XPATH, value='//select[@data-placeholder="Departments"]')

select = Select(select_element)

select.select_by_visible_text('Technology')
time.sleep(2)

links_set = set()


while driver.find_element(By.XPATH, '//div[@class="row loadmore"]').find_element(By.TAG_NAME, 'a').is_displayed():
    
    links = driver.find_elements(By.CLASS_NAME, 'h5')

    for li in links:
        links_set.add(li)

    driver.execute_script('arguments[0].click()', driver.find_element(By.XPATH, '//div[@class="row loadmore"]').find_element(By.TAG_NAME, 'a'))
    time.sleep(3)

job_data = []

for li in links_set:
    try:
        link = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
        driver.get(link)
        time.sleep(3)
        title = driver.find_element(By.TAG_NAME, 'h1').text
        location = driver.find_element(By.XPATH, '//div[@class="bottom"]').find_element(By.TAG_NAME, 'p').text
        about = driver.find_element(By.TAG_NAME, 'section').text
        job_data.append({'job_title' : str(title), 'job_location' : str(location), 'job_link' : str(link), 'job_desc' : str(about)})
    except:
        continue

print(json.dumps({"company":"optiver","data":job_data}))
driver.quit()