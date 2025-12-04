import json
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

TOP_K = 30  # nearest jobs

print("Loading job metadata...")
with open("backend/data/jobs_meta.json", "r", encoding="utf-8") as f:
    JOBS = json.load(f)
print("Loaded", len(JOBS), "jobs")

print("Loading SBERT model...")
EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading ANN index (PyNNDescent)...")
with open("backend/data/pynnd_index.pkl", "rb") as f:
    INDEX = pickle.load(f)

def recommend_jobs_sbert(resume_text, resume_skills):
    # 1. Encode resume
    r_emb = EMB_MODEL.encode(resume_text).astype("float32").reshape(1, -1)

    # 2. Query ANN index
    indices, distances = INDEX.query(r_emb, k=TOP_K)
    indices = indices[0]
    distances = distances[0]

    results = []
    rskills = set(resume_skills)

    for idx, dist in zip(indices, distances):
        job = JOBS[idx]

        # NNDescent with metric='cosine' => distance ≈ 1 - cosine_sim
        cos_sim = 1.0 - float(dist)
        jskills = job.get("skills_clean", [])
        overlap = len(rskills & set(jskills))

        title = (
            job.get("jobtitle_final")
            or job.get("jobtitle")
            or "Unknown Role"
        )

        results.append({
            "jobid": job["jobid"],
            "title": title,
            "match_score": round(cos_sim * 100, 2),
            "industry": job.get("industry", ""),
            "location": job.get("joblocation_address", ""),
            "skills_required": jskills,
            "skill_overlap": overlap,
        })

    # sort best first
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results
