# ml/scrape_jobs.py
import requests
import json
from time import sleep

API_URL = "https://example.com/api/jobs"  # replace with real / dataset loader

def fetch_jobs(num_pages=10):
    all_jobs = []
    for page in range(1, num_pages + 1):
        resp = requests.get(API_URL, params={"page": page})
        if resp.status_code != 200:
            break
        data = resp.json()
        for job in data["results"]:
            all_jobs.append({
                "job_id": job["id"],
                "title": job["title"],
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "description": job["description"],
                "raw_skills": job.get("skills", [])
            })
        sleep(0.5)  # don’t DDoS anything
    return all_jobs

if __name__ == "__main__":
    jobs = fetch_jobs()
    with open("data/raw_jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved {len(jobs)} jobs")
