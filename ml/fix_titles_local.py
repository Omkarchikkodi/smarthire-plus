import json
import re
from tqdm import tqdm

INPUT_FILE = "ml/data/jobs_with_emb.json"
OUTPUT_FILE = "ml/data/jobs_with_titles.json"

# Common skill → role mappings
SKILL_TO_ROLE = {
    "python": "Python Developer",
    "java": "Java Developer",
    "c++": "C++ Developer",
    "javascript": "JavaScript Developer",
    "react": "React Developer",
    "node": "Node.js Developer",
    "sql": "SQL Developer",
    "dba": "Database Administrator",
    "data": "Data Analyst",
    "ml": "Machine Learning Engineer",
    "machine learning": "Machine Learning Engineer",
    "deep learning": "Deep Learning Engineer",
    "nlp": "NLP Engineer",
    "cloud": "Cloud Engineer",
    "aws": "AWS Cloud Engineer",
    "devops": "DevOps Engineer",
    "embedded": "Embedded Engineer",
    "software": "Software Engineer",
    "full stack": "Full Stack Developer",
    "frontend": "Frontend Developer",
    "backend": "Backend Developer",
}

# Keyword → role fallback
DESC_KEYWORDS = {
    "developer": "Software Developer",
    "engineer": "Software Engineer",
    "analyst": "Data Analyst",
    "consultant": "IT Consultant",
    "manager": "Project Manager",
    "administrator": "System Administrator",
    "designer": "UI/UX Designer",
    "architect": "Software Architect",
}


def infer_from_skills(skills):
    if not skills:
        return None

    skills_lower = [s.lower() for s in skills]

    # Highest priority matching
    for key, role in SKILL_TO_ROLE.items():
        if any(key in s for s in skills_lower):
            return role

    return None


def infer_from_description(desc):
    if not desc:
        return None

    text = desc.lower()

    # Pattern-based extraction
    patterns = [
        r"looking for\s+([\w\s\-/]+)",
        r"hiring\s+([\w\s\-/]+)",
        r"role[:\-]\s*([\w\s\-/]+)",
        r"position[:\-]\s*([\w\s\-/]+)",
        r"job title[:\-]\s*([\w\s\-/]+)"
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            title = m.group(1).strip().title()
            if 3 < len(title) < 60:
                return title

    # Keyword based fallback
    for kw, role in DESC_KEYWORDS.items():
        if kw in text:
            return role

    return None


def infer_title(job):
    """
    Final title selection logic.
    Priority:
    1. Original title (if valid)
    2. Skill-based title
    3. Description keyword-based title
    4. Default: 'Software Engineer'
    """

    # 1. if original exists
    jt = job.get("jobtitle", "")
    if jt and len(jt.strip()) > 3:
        return jt.strip().title()

    # 2. from skills
    skills = job.get("skills_clean", []) or job.get("skills", [])
    title = infer_from_skills(skills)
    if title:
        return title

    # 3. from description
    title = infer_from_description(job.get("jobdescription", ""))
    if title:
        return title

    # 4. fallback
    return "Software Engineer"


# MAIN PROCESS
def main():
    print("Loading jobs...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        jobs = json.load(f)

    print(f"Total jobs: {len(jobs)}")

    updated = []
    for job in tqdm(jobs, desc="Inferring Titles"):
        job["jobtitle_final"] = infer_title(job)
        updated.append(job)

    print("\nSaving output...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2)

    print(f"✔ Done! Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
