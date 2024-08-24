from bs4 import BeautifulSoup
import requests
import time
import json


# def find_jobs_twosigma():
html_text = requests.get('https://careers.twosigma.com/').text
final_data = list()
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('article', class_='article article--card')
print(jobs)
for index, job in enumerate(jobs):
    print(job)
    job_name = job.find('a').text.strip()
    location = job.find('p').text.strip()
    job_link = job.find('a', class_="link")['href'].strip()
    final_data.append({
        "job_title": job_name,
        "job_location": location,
        "job_link": job_link
    })

json_data = json.dumps({"company": "twosigma", "data": final_data})
print(json_data)


# if __name__ == '__main__':
#     while True:
#         find_jobs_twosigma()
#         time_wait = 10
#         print(f'Waiting {time_wait} minutes...')
#         time.sleep(time_wait * 60)
