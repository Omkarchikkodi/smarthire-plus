import pdfplumber
import io
import json
import re
import os

SKILLS_PATH = os.path.join("backend", "skills_dict.json")
skills_list = json.load(open(SKILLS_PATH, "r"))

def parse_resume(data):
    text = ""

    # Try parsing PDF
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + " "
    except:
        text = data.decode("utf-8", errors="ignore")

    text_lower = text.lower()

    # Extract skills
    found_skills = []
    for skill in skills_list:
        if skill in text_lower:
            found_skills.append(skill)

    return text, found_skills
