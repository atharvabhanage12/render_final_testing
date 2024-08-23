import requests
from bs4 import BeautifulSoup
import json
categories=['4008242002','4043833002','4008241002','4008244002']
dict = {
        '4008242002':'Core Engineering',
        '4043833002':'On-Campus Recruiting',
        '4008241002':'Quantitative Research & Trading',
        '4008244002':'Systems & Network'
       }

req = requests.get("https://boards.greenhouse.io/alphagrepsecurities")
soup = BeautifulSoup(req.content, 'html.parser')
res = soup.find_all('section', class_="level-0")
finalsections=[]
for i in res:
    for j in categories:
        if str(j) in str(i):
            finalsections.append(i)

data=[]
for i in finalsections:
    soup1= BeautifulSoup(str(i), "html.parser")
    res1 = soup1.find_all('div', class_='opening')
    for j in res1:
        soup2 = BeautifulSoup(str(j), "html.parser")
        job_link=j.find('a')['href']
        job_title=j.find('a').text
        job_location=j.find('span').text
        job_department=j.get('department_id')  
        data.append({'job_title':job_title,'job_location':job_location,'job_department':dict[str(job_department)],'job_link':'https://boards.greenhouse.io'+job_link})

json_data=json.dumps({'company':'Alphagrep', 'data': data})
print(json_data)


L=json.loads(json_data)

output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "alphagrep", "data": L}, f, indent=4)
