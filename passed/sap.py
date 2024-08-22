from bs4 import BeautifulSoup
import requests
import json

# Send a GET request to the SAP job listings page
html_text = requests.get('https://jobs.sap.com/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_department=&optionsFacetsDD_customfield3=&optionsFacetsDD_country=').text

final_data = []
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('tr', class_='data-row')

# Extract job details
for job in jobs:
    job_name = job.find('a', class_="jobTitle-link").text.strip()
    location = job.find('span', class_="jobLocation").text.strip()
    job_link = job.find('a', class_="jobTitle-link")['href'].strip()
    
    final_data.append({
        "job_title": job_name,
        "job_location": location,
        "job_link": "https://jobs.sap.com/" + job_link
    })

# Save the collected job listings as JSON
output_path = "/opt/render/project/src/output1.json"
with open(output_path, "w") as f:
    json.dump({"company": "sap", "data": final_data}, f, indent=4)

print(f"Data saved to JSON: {output_path}")
