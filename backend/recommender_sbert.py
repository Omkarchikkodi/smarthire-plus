import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# -------- Paths --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")

JOBS_PATH = os.path.join(DATA_DIR, "jobs_with_titles.json")
INDEX_PATH = os.path.join(DATA_DIR, "pynnd_index.pkl")
RANKER_PATH = os.path.join(MODELS_DIR, "ranker_lightgbm.pkl")

print("Loading job data from:", JOBS_PATH)
with open(JOBS_PATH, "r", encoding="utf-8") as f:
    JOBS = json.load(f)

print("Sample loaded title:", JOBS[0].get("jobtitle_final", JOBS[0].get("jobtitle", "")))

print("Loading embedding model...")
EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading ANN index (PyNNDescent) from:", INDEX_PATH)
with open(INDEX_PATH, "rb") as f:
    INDEX = pickle.load(f)

print("Loading LightGBM ranker from:", RANKER_PATH)
with open(RANKER_PATH, "rb") as f:
    RANKER = pickle.load(f)

TOP_K = 30  # top nearest jobs


def recommend_jobs_sbert(resume_text, resume_skills):
    # 1. Encode resume
    r_emb = EMB_MODEL.encode(resume_text).astype("float32")

    # 2. Query ANN index
    indices, distances = INDEX.query(r_emb.reshape(1, -1), k=TOP_K)
    indices = indices[0]

    features = []
    selected_jobs = []

    for idx in indices:
        job = JOBS[idx]

        job_emb = np.array(job["embedding"]).reshape(1, -1)
        cos_sim = float(cosine_similarity(r_emb.reshape(1, -1), job_emb)[0][0])

        # skill overlap
        jskills = job.get("skills_clean", [])
        rskills = set(resume_skills)
        overlap_ratio = 0.0
        if jskills and resume_skills:
            overlap_ratio = len(rskills & set(jskills)) / len(rskills | set(jskills))

        # simple title match feature (you can tune this)
        title = job.get("jobtitle_final") or job.get("jobtitle") or ""
        title_lower = title.lower()
        title_match = int(any(k in title_lower for k in ["engineer", "developer", "analyst", "data"]))

        features.append([cos_sim, overlap_ratio, title_match])
        selected_jobs.append(job)

    X = np.array(features)
    scores = RANKER.predict(X)

    ranked = sorted(
        zip(selected_jobs, scores),
        key=lambda x: x[1],
        reverse=True,
    )

    results = []
    for job, score in ranked:
        title = job.get("jobtitle_final") or job.get("jobtitle") or "Unknown Role"
        results.append(
            {
                "jobid": job["jobid"],
                "title": title,
                "match_score": float(round(score, 2)),
                "industry": job.get("industry", ""),
                "location": job.get("joblocation_address", ""),
                "skills_required": job.get("skills_clean", []),
            }
        )

    return results
