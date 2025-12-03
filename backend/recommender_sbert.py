import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

JOBS = json.load(open(os.path.join(DATA_DIR, "jobs_with_titles.json"), "r", encoding="utf-8"))

EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

with open(os.path.join(DATA_DIR, "pynnd_index.pkl"), "rb") as f:
    INDEX = pickle.load(f)

TOP_K = 30

def recommend_jobs_sbert(resume_text, resume_skills):
    r_emb = EMB_MODEL.encode(resume_text).astype("float32")

    indices, distances = INDEX.query(r_emb.reshape(1, -1), k=TOP_K)
    indices = indices[0]

    results = []
    rskills = set(resume_skills)

    for idx in indices:
        job = JOBS[idx]

        job_emb = np.array(job["embedding"]).reshape(1, -1)
        cos_sim = float(cosine_similarity(r_emb.reshape(1, -1), job_emb)[0][0])

        jskills = job.get("skills_clean", [])
        overlap = len(rskills & set(jskills))

        results.append({
            "title": job.get("jobtitle_final") or job.get("jobtitle"),
            "match_score": round(cos_sim * 100, 2),
            "skills_required": jskills,
            "skill_overlap": overlap,
            "industry": job.get("industry", ""),
            "location": job.get("joblocation_address", "")
        })

    return sorted(results, key=lambda x: x["match_score"], reverse=True)
