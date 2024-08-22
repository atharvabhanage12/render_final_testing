from bs4 import BeautifulSoup
import requests
import json

# Fetch the HTML content of the job page
html_text = requests.get('https://www.quantboxresearch.com/jobs').text

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_text, 'html.parser')

print(html_text)
# Find all job items
jobs = soup.find_all('div', class_="job-item col-lg-12 col-md-12 col-sm-12 preview-highlighter")
final_data = []
print(jobs)
# Iterate through each job item to extract the desired information
for job in jobs:
    job_name = job.find('h3', class_='job-title').text.strip()
    location = job.find('div', class_='job-sub-title').find_all('small')[0].text.strip()
    job_code = job.find('div', class_='job-sub-title').find_all('small')[1].text.strip()
    job_link = job.find('h3', class_='job-title').a['href']

    final_data.append({
        "job_title": job_name,
        "job_location": location,
        "job_code": job_code,
        "job_link": "https://www.quantboxresearch.com" + job_link
    })

# Convert the final data to JSON format
json_data = json.dumps({"company": "quantbox", "data": final_data}, indent=4)

# Print the JSON output
print(json_data)
