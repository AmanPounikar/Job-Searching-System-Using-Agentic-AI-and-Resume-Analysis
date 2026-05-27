import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

params = {
    "query": "software developer",
    "page": "1",
    "num_pages": "1"
}

response = requests.get(url, headers=headers, params=params)

print("Status Code:", response.status_code)

data = response.json()

print("Keys:", data.keys())

jobs = data.get("data", [])

print("Number of jobs:", len(jobs))

if jobs:
    print("Sample Job Title:", jobs[0].get("job_title"))
else:
    print("❌ No jobs returned")