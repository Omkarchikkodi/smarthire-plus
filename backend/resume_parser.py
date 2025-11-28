import pdfplumber
import io
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

skills_list = json.load(
    open(os.path.join(BASE_DIR, "skills_dict.json"), "r", encoding="utf-8")
)


def parse_resume(data):
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + " "
    except Exception:
        text = data.decode("utf-8", errors="ignore")

    text_lower = text.lower()

    found_skills = []
    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill)

    return text, found_skills
