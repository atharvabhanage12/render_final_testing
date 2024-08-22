import requests
from bs4 import BeautifulSoup
import json

url = "https://jobs.lever.co/kpmgnz?Audit="
req = requests.get(url)
soup = BeautifulSoup(req.content, "html.parser")

# Parsing the job titles, links, and locations
job_titles = soup.find_all(attrs={"data-qa": "posting-name"})
job_links = soup.find_all(class_="posting-title")
job_locations = soup.find_all(class_="sort-by-location posting-category small-category-label location")

data = []
for i in range(len(job_titles)):
    job_data = {
        "job_title": job_titles[i].text,
        "job_link": job_links[i]["href"],
        "job_location": job_locations[i].text
    }
    data.append(job_data)

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "kpmg", "data": data}, f, indent=4)

print(f"Data saved to JSON: {output_path}")
