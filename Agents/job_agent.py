import os
import sys
from dotenv import load_dotenv
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer

# path fix — to access Modules folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Modules'))

from resume_parser import extract_text_from_pdf
from preprocessor import preprocess_text
from job_fetcher import fetch_jobs
from job_matcher import match_jobs

load_dotenv(dotenv_path="C:/Codes/Project main folder/.env")

# GROQ client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔥 NEW — dynamic role detection (no predefined roles)
def detect_role(text):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=10,
        ngram_range=(1, 2)
    )

    X = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()

    cleaned = []

    for word in keywords:
        if any(char.isdigit() for char in word):
            continue
        if len(word) < 4:
            continue

        cleaned.append(word)

    role_words = cleaned[:2]

# 🔥 remove duplicate WORDS safely
    words = []
    for w in role_words:
        for part in w.split():
            if part not in words:
                words.append(part)

    role = " ".join(words)

    return role if role else "jobs"


def generate_explanation(resume_text, job):
    prompt = f"""
Resume summary: {resume_text[:300]}

Job Title: {job['job_title']}
Job Description: {(job.get('job_description') or '')[:300]}
Match Score: {job['match_score']}

In 2-3 lines, explain why this job matches the resume.
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception:
        return "This job matches based on similarity between your skills and the job requirements."


def run_agent(resume_path):
    print("Step 1: Parsing resume...")
    raw_text = extract_text_from_pdf(resume_path)

    print("Step 2: Cleaning text...")
    clean_text = preprocess_text(raw_text)

    # 🔥 HYBRID ROLE SYSTEM
    print("Step 3: Detecting job role...")
    detected_role = detect_role(clean_text)

    print(f"Detected Role: {detected_role}")

    choice = input("Do you want to use this role? (y/n): ").strip().lower()

    if choice == "n":
        user_role = input("Enter desired job role: ").strip()
        final_role = user_role if user_role else detected_role
    else:
        final_role = detected_role

    print(f"Final Role Used: {final_role}")

    # 🔥 LOCATION FILTER
    country = input("Enter country (e.g. india, usa, uk): ").strip()
    location = input("Enter city (optional, press enter to skip): ").strip()

    # 🔥 SAFE QUERY BUILDING
    search_query = final_role

    if location:
        search_query += f" {location}"

    if country:
        search_query += f" {country}"

    print(f"Search Query: {search_query}")

    # 🔥 FETCH JOBS
    print("Step 4: Fetching jobs...")
    jobs = fetch_jobs(search_query)

    # 🔥 FALLBACK SYSTEM
    if not jobs:
        print("Fallback 1: trying only role...")
        jobs = fetch_jobs(final_role)

    if not jobs:
        print("Fallback 2: trying generic jobs...")
        jobs = fetch_jobs("jobs")

    if not jobs:
        print("Fallback 3: forcing default role...")
        jobs = fetch_jobs("assistant")

    # 🔥 MATCHING
    print("Step 5: Matching jobs...")
    top_jobs = match_jobs(clean_text, jobs)

    print("\n===== TOP 5 JOB MATCHES =====\n")
    for i, job in enumerate(top_jobs, 1):
        print(f"{i}. {job['job_title']} at {job['employer_name']}")
        print(f"   Match Score: {job['match_score']}")
        explanation = generate_explanation(raw_text, job)
        print(f"   Why: {explanation}")
        print()


if __name__ == "__main__":
    run_agent("Resumes/sample_resume.pdf")