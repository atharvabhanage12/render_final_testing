import requests
from bs4 import BeautifulSoup
import json

url = "https://jobsindia.deloitte.com/search/?q=&q2=&alertId=&locationsearch=&title=Technology&location=&date="

req = requests.get(url)
soup = BeautifulSoup(req.content,"html.parser")
j = str(soup.find_all("a"))
sp = str(soup.find_all("span"))
s = BeautifulSoup(j,"html.parser")
span = BeautifulSoup(sp,"html.parser")
data_row = s.find_all(class_="jobTitle-link")
location = span.find_all(class_="jobLocation visible-phone")

data=[]
for i in range(len(data_row)):
    jobs = {
        "job_title":data_row[i].text,
        "job_link":"https://jobsindia.deloitte.com/"+data_row[i]["href"],
        "job_location":location[0].text

    }
    data.append(jobs)
json_data = json.dumps({"company":"deloitte","data":data})
L= json.loads(json_data)
# print(json_data)
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump(json.loads({"company": "deloitte", "data": L}), f, indent=4)
print(L)