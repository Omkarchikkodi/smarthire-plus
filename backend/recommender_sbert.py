import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Loading job data...")
JOBS = json.load(open(
    os.path.join(BASE_DIR, "data", "jobs_with_titles.json"),
    "r",
    encoding="utf-8"
))

print("Sample loaded title:", JOBS[0].get("jobtitle_final", ""))

print("Loading embedding model...")
EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading ANN index (PyNNDescent)...")
with open(os.path.join(BASE_DIR, "data", "pynnd_index.pkl"), "rb") as f:
    INDEX = pickle.load(f)

TOP_K = 30  # top nearest jobs


def recommend_jobs_sbert(resume_text, resume_skills):
    # 1. Encode resume
    r_emb = EMB_MODEL.encode(resume_text).astype("float32")

    # 2. Query ANN
    indices, distances = INDEX.query(r_emb.reshape(1, -1), k=TOP_K)
    indices = indices[0]

    results = []

    for idx in indices:
        job = JOBS[idx]

        # cosine similarity
        job_emb = np.array(job["embedding"]).reshape(1, -1)
        cos_sim = float(
            cosine_similarity(r_emb.reshape(1, -1), job_emb)[0][0]
        )

        # skill overlap
        jskills = job.get("skills_clean", [])
        rskills = set(resume_skills)
        overlap = len(rskills & set(jskills))

        # final title
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
            "skill_overlap": overlap
        })

    # Sort best first
    results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    return results
