import streamlit as st
import os
import tempfile

from resume_parser import extract_text_from_pdf
from preprocessor import preprocess_text
from job_fetcher import fetch_jobs
from job_matcher import match_jobs

from groq import Groq
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer

# Load env
load_dotenv(dotenv_path="C:/Codes/Project main folder/.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- UI CONFIG ----------------
st.set_page_config(
    page_title="AI Job Matcher",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
}

.stButton>button {
    background: linear-gradient(90deg, #22c55e, #4ade80);
    color: black;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

.stTextInput>div>div>input {
    background-color: #1e293b;
    color: white;
}

.job-card {
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #334155;
}

.match-score {
    color: #22c55e;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align: center;'>🚀 AI Job Recommendation System</h1>
<p style='text-align: center; color: gray;'>Find the best jobs based on your resume using AI</p>
""", unsafe_allow_html=True)



# ---------------- FUNCTIONS ----------------
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

Explain in 2-3 lines why this job matches the resume.
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        return "Good match based on skills and job description."


# ---------------- MAIN UI ----------------

uploaded_file = st.file_uploader("📄 Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        resume_path = tmp.name

    st.success("✅ Resume uploaded successfully!")

    # Process resume
    raw_text = extract_text_from_pdf(resume_path)
    clean_text = preprocess_text(raw_text)

    # Detect role
    detected_role = detect_role(clean_text)

    st.subheader("🧠 Detected Role")
    st.write(detected_role)

    # User input
    user_role = st.text_input("✏️ Edit Role", detected_role)

    col1, col2 = st.columns(2)

    with col1:
        country = st.text_input("🌍 Country")

    with col2:
        location = st.text_input("📍 City (optional)")

    if st.button("🔍 Find Jobs"):
        with st.spinner("Fetching jobs..."):
            final_role = user_role if user_role else detected_role

            search_query = final_role
            if location:
                search_query += f" {location}"
            if country:
                search_query += f" {country}"

            jobs = fetch_jobs(search_query)

            if not jobs:
                jobs = fetch_jobs(final_role)

            if not jobs:
                jobs = fetch_jobs("jobs")

            if not jobs:
                st.error("❌ No jobs found. Try different input.")
                st.stop()

            top_jobs = match_jobs(clean_text, jobs)

        st.success("✅ Top Matches Found!")
        st.subheader("🎯 Top Job Matches")

        # Display jobs
        for i, job in enumerate(top_jobs, 1):
            st.markdown(f"""
            <div class="job-card">
                <h3>#{i} {job['job_title']}</h3>
                <p>🏢 {job['employer_name']}</p>
                <p class="match-score">📊 Match Score: {round(job['match_score'], 2)}</p>
            </div>
            """, unsafe_allow_html=True)

            explanation = generate_explanation(raw_text, job)
            st.info(f"💡 {explanation}")

            # streamlit run "c:/Codes/Project main folder/Modules/app(classic).py"