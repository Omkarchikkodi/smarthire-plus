import pandas as pd
import json
import re
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# === LOAD JOB DATASET ===
df = pd.read_csv("ml/job_samples.csv")

print("Loaded rows:", len(df))

# === CLEANING HELPERS ===

def clean_text(t):
    if pd.isna(t):
        return ""
    t = str(t)
    t = re.sub(r"\s+", " ", t)
    t = t.replace("\u00a0", " ")
    return t.strip()


def extract_title(row):
    """Return jobtitle if available; otherwise infer from jobdescription."""
    title = clean_text(row.get("jobtitle", ""))

    # Use provided title if valid
    if title and len(title) > 3:
        return title

    desc = clean_text(row.get("jobdescription", "")).lower()

    # Regex patterns to infer job role
    patterns = [
        r"looking for (a|an)?\s*([\w\s\-/]+)",
        r"hiring\s*([\w\s\-/]+)",
        r"role[:\-]\s*([\w\s\-/]+)",
        r"position[:\-]\s*([\w\s\-/]+)",
        r"job\s*title[:\-]\s*([\w\s\-/]+)",
    ]

    for p in patterns:
        m = re.search(p, desc)
        if m:
            role = m.group(len(m.groups()))
            role = role.strip().title()
            if 3 < len(role) < 60:
                return role

    # Keyword fallback
    common_roles = [
        "developer", "engineer", "analyst", "manager", "consultant",
        "administrator", "specialist", "scientist", "designer", "lead"
    ]

    for word in common_roles:
        if word in desc:
            return word.title()

    # Fallback: First line of description
    first_line = row.get("jobdescription", "").split("\n")[0].strip()
    if len(first_line) > 10:
        return first_line[:80]

    return "Unknown Role"


def clean_skills(skill_str):
    if pd.isna(skill_str):
        return []
    s = skill_str.lower()
    s = re.sub(r"[^a-z0-9,+\- ]", " ", s)
    parts = re.split(r"[,+]| and | or ", s)
    cleaned = sorted(set([p.strip() for p in parts if len(p.strip()) > 1]))
    return cleaned


def extract_experience(exp_text):
    if pd.isna(exp_text):
        return (0, 0)
    exp = str(exp_text)
    match = re.findall(r"(\d+)\s*-\s*(\d+)", exp)
    if match:
        return (int(match[0][0]), int(match[0][1]))
    n = re.findall(r"(\d+)\s*yrs?", exp)
    if n:
        return (int(n[0]), int(n[0]))
    return (0, 0)


# === EMBEDDING MODEL ===
model = SentenceTransformer("all-MiniLM-L6-v2")

# === PROCESS JOBS ===
processed = []

for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing jobs"):

    title = extract_title(row)
    desc = clean_text(row.get("jobdescription", ""))
    skills = clean_skills(row.get("skills", ""))

    exp_min, exp_max = extract_experience(row.get("experience", ""))

    # Text for embedding
    text_for_emb = f"{title}. {desc} Skills: {', '.join(skills)}"

    emb = model.encode(text_for_emb).tolist()

    processed.append({
        "jobid": row["jobid"],
        "jobtitle": title,
        "jobdescription": desc,
        "skills_clean": skills,
        "industry": clean_text(row.get("industry", "")),
        "education": clean_text(row.get("education", "")),
        "joblocation_address": clean_text(row.get("joblocation_address", "")),
        "exp_min": exp_min,
        "exp_max": exp_max,
        "embedding": emb
    })


# === SAVE OUTPUT ===
out_path = "ml/data/jobs_with_titles.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(processed, f, indent=2)

print("\n✔ DONE!")
print(f"✔ Cleaned & embedded file saved: {out_path}")
print(f"✔ Total processed jobs: {len(processed)}")
