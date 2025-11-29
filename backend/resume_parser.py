import pdfplumber
import io
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_PATH = os.path.join(BASE_DIR, "backend", "skills_dict.json")

with open(SKILLS_PATH, "r", encoding="utf-8") as f:
    skills_list = json.load(f)


def parse_resume(data: bytes):
    # PDF → TEXT
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + " "
    except Exception:
        # fallback if it's not a PDF
        text = data.decode("utf-8", errors="ignore")

    text_lower = text.lower()

    found_skills = []
    for skill in skills_list:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    # deduplicate while preserving order
    seen = set()
    unique_skills = []
    for s in found_skills:
        if s not in seen:
            seen.add(s)
            unique_skills.append(s)

    return text, unique_skills
