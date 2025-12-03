from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.resume_parser import parse_resume
from backend.recommender_sbert import recommend_jobs_sbert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "SmartHire+ API Running"}

@app.post("/resume/recommend-sbert")
async def recommend_resume_sbert(file: UploadFile):
    data = await file.read()
    text, skills = parse_resume(data)

    results = recommend_jobs_sbert(text, skills)
    return {"results": results}
