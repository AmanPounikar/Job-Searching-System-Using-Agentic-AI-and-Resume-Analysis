import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")


def fetch_jobs(query):
    url = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": "1"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # 🔥 DEBUG PRINT
        print("API Response keys:", data.keys())

        jobs = data.get("data", [])

        # 🔥 If empty → debug
        if not jobs:
            print("⚠️ No jobs returned from API for query:", query)

        return jobs

    except Exception as e:
        print("API Error:", e)
        return []