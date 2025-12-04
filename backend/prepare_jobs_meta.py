import json
import os

SRC = os.path.join(os.path.dirname(__file__), "data", "jobs_with_titles.json")
DST = os.path.join(os.path.dirname(__file__), "data", "jobs_meta.json")

print("Loading:", SRC)
with open(SRC, "r", encoding="utf-8") as f:
    jobs = json.load(f)

meta = []
for j in jobs:
    meta.append({
        "jobid": j["jobid"],
        "jobtitle_final": j.get("jobtitle_final") or j.get("jobtitle") or "",
        "industry": j.get("industry", ""),
        "joblocation_address": j.get("joblocation_address", ""),
        "skills_clean": j.get("skills_clean", []),
    })

print("Jobs:", len(meta))
print("Saving to:", DST)
with open(DST, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False)

print("Done.")
