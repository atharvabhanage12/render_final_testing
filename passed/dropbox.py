import requests
import json
from bs4 import BeautifulSoup

def scrape_job_positions():
    url = "https://jobs.dropbox.com/all-jobs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    job_positions = []
    job_elements = soup.find_all("div", class_="open-positions__listing-group open-positions__listing-group--left")
    # print(job_elements)
    
    for element in job_elements:
        for x in element.find_all("li", class_="open-positions__listing"):
            job_category = element.find("a", class_="open-positions__dept-title-link").text.strip()
            job_location = x.find("p", class_="open-positions__listing-location").text.strip()
            job_title = x.find("h5", class_="open-positions__listing-title").text.strip()
            
            job_positions.append({
                "job_title": job_title,
                "job_location": job_location,
                "job_category": job_category,
                "job_link":'https://jobs.dropbox.com/all-jobs'
        })
    
    return job_positions

# def save_to_json(data, filename):
#     with open(filename, "w") as file:
#         json.dump(data, file, indent=4)

# Scrape job positions
job_positions = scrape_job_positions()

# Save job positions to JSON file
# save_to_json(job_positions, "DropBoxData.json")
print(json.dumps({"company":"dropbox","data":job_positions}))

output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "microsoft", "data": job_positions}, f, indent=4)