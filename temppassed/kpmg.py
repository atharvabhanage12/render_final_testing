import requests
from bs4 import BeautifulSoup
import json

url = "https://jobs.lever.co/kpmgnz?department=Corporate%20Services&team=IT"

req = requests.get(url)

soup = BeautifulSoup(req.content,"html.parser")
j = str(soup.find_all("h5"))
a = str(soup.find_all("a"))
s = str(soup.find_all("span"))
# # p = str(soup.find_all("p"))
# # l = str(soup.find_all("li"))
job_obj = BeautifulSoup(j,"html.parser")
link_obj = BeautifulSoup(a,"html.parser")
loc_obj = BeautifulSoup(s,"html.parser")
# # loc = BeautifulSoup(p,"html.parser")
# # lst = BeautifulSoup(l,"html.parser")
jobs = job_obj.find_all(attrs={"data-qa":"posting-name"})
links = link_obj.find_all(class_="posting-title")
locations = loc_obj.find_all(class_="sort-by-location posting-category small-category-label location")


data=[]
for i in range(len(jobs)):
    job_data = {
        "job_title":jobs[i].text,
        "job_link":links[i]["href"],
        "job_location":links[i].text

    }
    data.append(job_data)
json_data = json.dumps({"company":"kpmg","data":data})
print(json_data)
# driver.quit()