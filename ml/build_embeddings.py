import json
from sentence_transformers import SentenceTransformer
import numpy as np
import os

MODEL_NAME = "all-MiniLM-L6-v2"

def main():
    # Load dataset
    jobs = json.load(open("data/processed_jobs.json"))

    print(f"Loaded {len(jobs)} jobs")
    model = SentenceTransformer(MODEL_NAME)

    # Extract text
    texts = [job["text"] for job in jobs]

    print("Generating embeddings...")
    embs = model.encode(texts, batch_size=32, show_progress_bar=True)

    # Attach embeddings to job records
    for job, emb in zip(jobs, embs):
        job["embedding"] = emb.tolist()

    # Save output file
    out_path = "ml/data/jobs_with_emb.json"
    json.dump(jobs, open(out_path, "w"), indent=2)

    print(f"✔ Embeddings saved to {out_path}")

if __name__ == "__main__":
    main()
