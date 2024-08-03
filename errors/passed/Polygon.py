import requests
from bs4 import BeautifulSoup
import json

req = requests.get("https://jobs.lever.co/Polygon/?department=Engineering")
soup = BeautifulSoup(req.content, "html.parser")
res1 = soup.find_all("div", class_='posting')
# print(res1)
# print(len(res1))
final_divs=[]
for i in res1:
    # print(i)
    soup1 = BeautifulSoup(str(i), "html.parser")
    # print("\n")
    # res2 = soup1.find('div',class_='sort-by-team posting-category small-category-label department').text
    final_divs.append(i)
    # # print(res2)
    # if "Tech" in str(res2):
    #     # print(res2)
    #     final_divs.append(i)


        
       
data = []
for i in final_divs:
    soup2 = BeautifulSoup(str(i),"html.parser")
    job_link= soup2.find('a')["href"]
    job_title= soup2.find(attrs={"data-qa":"posting-name"}).text
    job_location= soup2.find(attrs={"class":"sort-by-location posting-category small-category-label location"}).text
    job_commitment = soup2.find(class_="sort-by-commitment posting-category small-category-label commitment").text
    work_place_type = soup2.find(attrs={"class":"display-inline-block small-category-label workplaceTypes"}).text
    # job_department = soup2.find(attrs={"class":"sort-by-team posting-category small-category-label department"}).text.replace("\u2013","-")
    data.append({"job_title":str(job_title),"job_location":str(job_location),"job_commitment":str(job_commitment),"work_place_type":str(work_place_type),"job_link":str(job_link)})
# json_data = json.dumps(data)
json_data = json.dumps({"company":"polygon","data":data})
print(json_data)







