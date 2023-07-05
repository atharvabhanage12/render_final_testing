from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import json
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
chrome_options = Options()
chrome_options.binary_location = './firefox.exe'
chrome_options.add_argument("--headless")
website = "https://www.janestreet.com/join-jane-street/open-roles/?type=students-and-new-grads&location=all-locations&department=technology"

driver = webdriver.Firefox(options=chrome_options,service=FirefoxService(GeckoDriverManager().install()))

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