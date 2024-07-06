import os
import subprocess
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Run the script and capture the output
result = subprocess.run(['./script.sh'], capture_output=True, text=True)

# Print the captured stdout and stderr
print("ATHARVA DEBUG: script.sh output")
print(result.stdout)
print(result.stderr)

chromium_path = "/opt/render/project/.render/chrome/opt/google/chrome"
chromedriver_path = "/opt/render/project/.render/chrome/opt/google/chrome/chromedriver"  # Adjust the path if necessary

print("ATHARVA DEBUG: chromium_path")
print(chromium_path)
print("ATHARVA DEBUG: chromedriver_path")
print(chromedriver_path)

# Add the Chromium path to the PATH environment variable
os.environ['PATHCHROME'] = chromium_path
os.environ["PATH"] += ":" + chromedriver_path

# Verify the updated PATH
print("ATHARVA DEBUG: Updated PATH")
print(os.environ['PATH'])

# Selenium setup
firefox_options = Options()
firefox_options.binary_location = chromium_path
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")

service = Service(chromedriver_path)
driver = webdriver.Chrome(options=firefox_options, service=service)

url = "https://www.yahooinc.com/careers/search.html"
driver.get(url)
driver.implicitly_wait(20)
time.sleep(3)

L = []
soup = BeautifulSoup(driver.page_source, "html.parser")
var0 = driver.find_element(By.XPATH, "//button[@data-target='#collapseJC']")
driver.execute_script("arguments[0].click()", var0)
time.sleep(2)
elem = driver.find_elements(By.XPATH, "//input[@class='custom-control-input']")
for i in elem:
    var1 = i.get_attribute("id")
    if var1 in ["engineering", "softwaredevelopment", "design", "informationsystems", "internship", "research"]:
        driver.execute_script("arguments[0].click()", i)

submit = driver.find_element(By.XPATH, "//button[@id='search-page-find-jobs']")
driver.execute_script("arguments[0].click()", submit)
time.sleep(3)

L = []
while True:
    try:
        elem = driver.find_element(By.XPATH, "//button[@class='btn my-3 loadMore']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(2)
    except:
        break

    sentence = driver.find_element(By.XPATH, "//p[@class='resultsTotal']").text
    ns = ""
    for i in sentence:
        if i not in "0123456789":
            if ns != "":
                break
        else:
            ns += i
    sn = ""
    i = len(sentence) - 1
    while True:
        if sentence[i] in "0123456789":
            sn = sentence[i] + sn
            i -= 1
        else:
            break
    if ns == sn:
        break

soup2 = BeautifulSoup(driver.page_source, "html.parser")
total = soup2.find_all("tr", class_='jobTitle')

script = """
    var elements = document.querySelectorAll("a");
    var href = [];
    for (var i = 0 ; i< elements.length; i++){
        href.push(elements[i].href);
    }
    return href;
"""
L1 = driver.execute_script(script)
hrefs = [i for i in L1 if "/careers/job/" in i]

count = 0
for i in total:
    soup3 = BeautifulSoup(str(i), "html.parser")
    job_title = soup3.find("td", class_='col-6').text
    job_link = hrefs[count]
    job_location = soup3.find("div", class_="tableLocPrimary").text
    L.append({"job_title": job_title, "job_location": job_location, "job_link": job_link})
    count += 1

json_data = json.dumps({"company": "yahoo", "data": L})
print(json_data)
driver.quit()
