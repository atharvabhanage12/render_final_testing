from bs4 import BeautifulSoup
import requests
import time
import json


# def find_jobs_sap():
html_text = requests.get('https://jobs.sap.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_department=&optionsFacetsDD_customfield3=&optionsFacetsDD_country=').text
final_data = list()
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('tr', class_='data-row')
# print(jobs)
for index, job in enumerate(jobs):
    job_name = job.find('a', class_="jobTitle-link").text.strip()
    location = job.find('span', class_="jobLocation").text.strip()

    job_link = job.find('a', class_="jobTitle-link")['href'].strip()
    final_data.append({
        "job_title": job_name,
        "job_location": location,
        "job_link": "https://jobs.sap.com/"+job_link
    })

json_data = json.dumps({"company": "sap", "data": final_data})
print(json_data)


# if __name__ == '__main__':
#     while True:
#         find_jobs_sap()
#         time_wait = 10
#         print(f'Waiting {time_wait} minutes...')
#         time.sleep(time_wait * 60)
