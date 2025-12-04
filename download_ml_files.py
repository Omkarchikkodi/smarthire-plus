import os
import gdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

FILES = [
    # Small metadata (all jobs, no embeddings)
    {
        "id": "1ywm2Q81shpYH__gNwcsLCsxZhgv9-PFh",          # <-- REPLACE
        "out": os.path.join(DATA_DIR, "jobs_meta.json"),
        "name": "jobs_meta.json",
    },
    # ANN index (same as before)
    {
        "id": "1XNGbX6vGiQyqF0Q1mv9vbpBEIKJk1WDj",
        "out": os.path.join(DATA_DIR, "pynnd_index.pkl"),
        "name": "pynnd_index.pkl",
    },
    # LightGBM model (optional but small)
    {
        "id": "1aqnt3HM4Ho_uhtrS45SvnpkoJP_xEZ-s",
        "out": os.path.join(MODELS_DIR, "ranker_lightgbm.pkl"),
        "name": "ranker_lightgbm.pkl",
    },
]

def download_if_missing(file_id: str, out_path: str, name: str):
    if os.path.exists(out_path):
        print(f"[SKIP] {name} already exists at {out_path}")
        return
    print(f"[DOWNLOAD] {name} -> {out_path}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, out_path, quiet=False)

if __name__ == "__main__":
    print("=== Downloading ML artifacts ===")
    for f in FILES:
        download_if_missing(f["id"], f["out"], f["name"])
    print("=== Done ===")
