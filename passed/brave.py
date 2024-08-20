import requests
import json
from bs4 import BeautifulSoup

def scrape_job_positions():
    url = "https://boards.greenhouse.io/embed/job_board?for=brave&amp;b=https%3A%2F%2Fbrave.com%2Fcareers%2F"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    job_positions = []
    job_elements = soup.find_all("section", class_="level-0")
    
    for element in job_elements:
        for x in element.find_all("div", class_="opening"):
            job_category = element.find("h3").text.strip()
            job_location = x.find("span", class_="location").text.strip()
            job_title = x.find("a").text.strip()
            
            job_positions.append({
                "job_title": job_title,
                "job_location": job_location,
                "job_category": job_category,
                "job_link":'https://brave.com/careers/'
        })
    
    return job_positions

def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Scrape job positions
job_positions = scrape_job_positions()

# Save job positions to JSON file
# save_to_json(job_positions, "BraveData.json")
fin = json.dumps({"company":"brave","data":job_positions})
print(fin)
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "microsoft", "data": fin}, f, indent=4)
