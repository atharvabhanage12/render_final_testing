import requests
from bs4 import BeautifulSoup
import json

req = requests.get("https://jobs.lever.co/clevertap?department=CLEVERTAP&team=Engineering")
soup = BeautifulSoup(req.content, 'html.parser')
res = soup.find_all('div', class_="posting")

data=[]
for j in res:
    job_link=j.find('a')['href']
    job_title=j.find('h5').text
    job_location=j.find('span', class_="sort-by-location posting-category small-category-label location").text
    job_department='Engineering'
    job_commitment = j.find('span', class_="sort-by-commitment posting-category small-category-label commitment").text
    job_workplace_type = j.find('span', class_='display-inline-block small-category-label workplaceTypes').text
    data.append({'job_title':job_title, 'job_location':job_location, 'job_department':job_department, 'job_commitment':job_commitment, 'job_workplace_type':job_workplace_type, 'job_link':job_link, })

json_data=json.dumps({'company':'clevertap', 'data': data})
print(json_data)
L=json.loads(json_data)
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "clevertap", "data": L}, f, indent=4)





