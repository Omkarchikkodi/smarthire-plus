import json
import numpy as np
import pandas as pd
import faiss
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ===============================
# CONFIG
# ===============================
JOBS_PATH = "ml/data/jobs_with_emb.json"
RESUMES_PATH = "ml/data/resumes_train.json"
OUTPUT_PATH = "ml/data/train_pairs.csv"

TOP_K = 120        # Candidate positive jobs
NEGATIVE_K = 25    # Random negative jobs per resume
EMBED_DIM = 384    # Dimension for all-MiniLM-L6-v2


# ===============================
# HELPER FUNCTIONS
# ===============================
def compute_skill_overlap(resume_skills, job_skills):
    if not resume_skills or not job_skills:
        return 0.0
    rs, js = set(resume_skills), set(job_skills)
    return len(rs & js) / len(rs | js)

def label_match(skill_overlap, cos_sim):
    if cos_sim >= 0.70 and skill_overlap >= 0.25:
        return 2   # strong match
    elif cos_sim >= 0.45 and skill_overlap >= 0.10:
        return 1   # partial match
    return 0       # weak


# ===============================
# MAIN PIPELINE
# ===============================
def main():
    print("Loading job dataset with embeddings…")
    jobs = json.load(open(JOBS_PATH))
    print(f"Loaded {len(jobs)} jobs")

    print("Loading resumes…")
    resumes = json.load(open(RESUMES_PATH))
    print(f"Loaded {len(resumes)} resumes")

    # -------------------------------
    # BUILD FAISS HNSW INDEX
    # -------------------------------
    print("Building FAISS HNSW index…")

    job_embs = np.array([j["embedding"] for j in jobs], dtype="float32")
    index = faiss.IndexHNSWFlat(EMBED_DIM, 64)  # HNSW with 64 neighbors
    index.hnsw.efConstruction = 80
    index.add(job_embs)

    print("FAISS index built ✓")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    rows = []

    # -------------------------------
    # PROCESS EACH RESUME
    # -------------------------------
    for r in resumes:
        rid = r["resume_id"]
        r_skills = r["skills"]
        target_roles = r["target_roles"]

        # Encode resume ONCE
        r_emb = model.encode(r["text"]).astype("float32").reshape(1, -1)

        # Query FAISS → Top-K jobs
        distances, indices = index.search(r_emb, TOP_K)

        top_indices = indices[0]
        top_jobs = [jobs[i] for i in top_indices]

        # Sample random negatives (avoid overlap)
        negatives = random.sample(
            [i for i in range(len(jobs)) if i not in top_indices],
            NEGATIVE_K
        )
        negative_jobs = [jobs[i] for i in negatives]

        # Positive examples
        for job in top_jobs:
            cos_sim = float(cosine_similarity(
                r_emb, np.array(job["embedding"]).reshape(1, -1)
            )[0][0])

            skill_overlap = compute_skill_overlap(
                r_skills, job.get("skills_clean", job.get("skills", []))
            )

            title_match = int(
                any(t.lower() in job["jobtitle"].lower() for t in target_roles)
            )

            label = label_match(skill_overlap, cos_sim)

            rows.append([
                rid,
                job["jobid"],
                cos_sim,
                skill_overlap,
                title_match,
                label
            ])

        # Negative examples → label=0 always
        for job in negative_jobs:
            rows.append([
                rid,
                job["jobid"],
                0.0,  # cos_sim
                0.0,  # skill overlap
                0,    # title match
                0     # label
            ])

        print(f"Processed resume {rid}")

    # -------------------------------
    # SAVE TRAINING DATA
    # -------------------------------
    df = pd.DataFrame(rows, columns=[
        "resume_id", "jobid", "cos_sim",
        "skill_overlap", "title_match", "label"
    ])

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"\n✔ Training dataset saved to {OUTPUT_PATH}")
    print("Total training rows:", df.shape[0])
    print("Done ✓")


if __name__ == "__main__":
    main()
