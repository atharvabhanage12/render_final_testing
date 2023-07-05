from bs4 import BeautifulSoup
import requests
import time
import json

html_text = requests.get('https://www.quantboxresearch.com/jobs').text
final_data = list()
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('div', class_='job-item')

for index, job in enumerate(jobs):
    job_name = job.find('h3', class_='job-title').text.strip()
    location = job.find('div', class_='job-sub-title').find('small').text.strip()
    job_link = job.h3.a['href']
    final_data.append({
        "job_title": job_name.strip(),
        "job_location": location.strip(),
        "job_link": "https://www.quantboxresearch.com"+job_link.strip()
    })

json_data = json.dumps({"company": "quantbox", "data": final_data})
print(json_data)
