import pdfplumber
import io
import json
import os

BASE_DIR = os.path.dirname(__file__)

skills_list = json.load(open(os.path.join(BASE_DIR, "skills_dict.json")))
       
def parse_resume(data):
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + " "
    except:
        text = data.decode("utf-8", errors="ignore")

    found_skills = [skill for skill in skills_list if skill in text.lower()]
    return text, found_skills
