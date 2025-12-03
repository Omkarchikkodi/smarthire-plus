import os
import gdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "backend", "data")
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

FILES = [
    {
        "id": "1l6TBKKckRWPS4eTl5R_b2J9QTikwePfM",
        "out": os.path.join(DATA_DIR, "jobs_with_titles.json"),
        "name": "jobs_with_titles.json",
    },
    {
        "id": "1PH1nFl6LtnOwuU0unGEIZPB9ACryloa5",
        "out": os.path.join(DATA_DIR, "jobs_with_emb.json"),
        "name": "jobs_with_emb.json",
    },
    {
        "id": "1XNGbX6vGiQyqF0Q1mv9vbpBEIKJk1WDj",
        "out": os.path.join(DATA_DIR, "pynnd_index.pkl"),
        "name": "pynnd_index.pkl",
    },
    {
        "id": "1aqnt3HM4Ho_uhtrS45SvnpkoJP_xEZ-s",
        "out": os.path.join(MODELS_DIR, "ranker_lightgbm.pkl"),
        "name": "ranker_lightgbm.pkl",
    },
]

def download_if_missing(file_id: str, out_path: str, name: str):
    if os.path.exists(out_path):
        print(f"[SKIP] {name} already exists.")
        return
    print(f"[DOWNLOAD] {name}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, out_path, quiet=False)

if __name__ == "__main__":
    print("=== Downloading ML artifacts ===")
    for f in FILES:
        download_if_missing(f["id"], f["out"], f["name"])
    print("=== Done ===")
