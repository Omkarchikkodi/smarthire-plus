import pandas as pd
import re
import json
import os

def normalize_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"Ã|Â|â|€|™|¢", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_skills(text):
    if not isinstance(text, str):
        return []
    text = text.lower()
    tech_skills = re.findall(r"[a-zA-Z\+\#\.]{2,}", text)
    return list(set(tech_skills))

def infer_target_roles(category, resume_text):
    category = category.lower()
    
    if "data" in category:
        return ["data scientist", "ml engineer", "nlp engineer"]
    if "software" in category or "developer" in resume_text.lower():
        return ["software developer", "backend engineer"]
    if "testing" in category:
        return ["software tester", "qa engineer"]
    if "cloud" in category:
        return ["cloud engineer", "devops engineer"]
    return ["general role"]

def main():
    df = pd.read_csv("ml/data/UpdatedResumeDataSet.csv")  # change filename if needed
    resumes = []

    for idx, row in df.iterrows():
        resume_text = normalize_text(str(row["Resume"]))
        category = normalize_text(str(row["Category"]))
        skills = extract_skills(resume_text)
        target_roles = infer_target_roles(category, resume_text)

        resumes.append({
            "resume_id": f"res_{idx+1:03}",
            "category": category,
            "text": resume_text,
            "skills": skills,
            "target_roles": target_roles
        })

    os.makedirs("ml/data", exist_ok=True)
    json.dump(resumes, open("ml/data/resumes_train.json", "w"), indent=2)
    print(f"✔ Saved {len(resumes)} formatted resumes to ml/data/resumes_train.json")

if __name__ == "__main__":
    main()
