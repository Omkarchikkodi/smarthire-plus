from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import parse_resume
from recommender_sbert import recommend_jobs_sbert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SmartHire+ API Running (SBERT Only)"}

@app.post("/resume/recommend-sbert")
async def recommend_resume_sbert(file: UploadFile):
    data = await file.read()
    text, skills = parse_resume(data)

    print("\n=== DEBUG ===")
    print("Resume length:", len(text))
    print("Skills sample:", skills[:20])
    print("=============\n")

    results = recommend_jobs_sbert(text, skills)

    return {"results": results}
