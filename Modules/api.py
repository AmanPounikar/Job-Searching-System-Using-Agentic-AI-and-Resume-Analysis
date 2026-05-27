from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os
from dotenv import load_dotenv
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer

from resume_parser import extract_text_from_pdf
from preprocessor import preprocess_text
from job_fetcher import fetch_jobs
from job_matcher import match_jobs

load_dotenv(dotenv_path="C:/Codes/Project main folder/.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def detect_role(text):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=10, ngram_range=(1, 2))
    vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    cleaned = [w for w in keywords if not any(c.isdigit() for c in w) and len(w) >= 4]
    role_words = cleaned[:2]
    words = []
    for w in role_words:
        for part in w.split():
            if part not in words:
                words.append(part)
    return " ".join(words) or "jobs"


def generate_explanation(resume_text, job):
    prompt = f"""
Resume summary: {resume_text[:300]}
Job Title: {job['job_title']}
Job Description: {(job.get('job_description') or '')[:300]}
Match Score: {job['match_score']}
Explain in 2-3 lines why this job matches the resume.
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "Good match based on skills and experience."


@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        path = tmp.name
    raw = extract_text_from_pdf(path)
    clean = preprocess_text(raw)
    role = detect_role(clean)
    os.unlink(path)
    return {"detected_role": role, "resume_text": raw, "clean_text": clean}


@app.post("/match-jobs")
async def match_jobs_endpoint(
    resume_text: str = Form(...),
    clean_text: str = Form(...),
    role: str = Form(...),
    country: str = Form(""),
    city: str = Form(""),
):
    query = role
    if city:
        query += f" {city}"
    if country:
        query += f" {country}"

    jobs = fetch_jobs(query) or fetch_jobs(role) or fetch_jobs("jobs")

    if not jobs:
        return {"jobs": []}

    top_jobs = match_jobs(clean_text, jobs)

    results = []
    for job in top_jobs:
        explanation = generate_explanation(resume_text, job)
        results.append({
            "job_title": job.get("job_title", ""),
            "employer_name": job.get("employer_name", ""),
            "match_score": job.get("match_score", 0),
            "job_description": job.get("job_description", ""),
            "explanation": explanation,
            "job_apply_link": job.get("job_apply_link", ""),
        })

    return {"jobs": results}
