# Job Searching System Using Agentic AI and Resume Analysis

An AI-powered job recommendation system that analyzes resumes, detects suitable job roles, and matches users with relevant job opportunities.

## Features

- Resume PDF parsing
- AI-based role detection
- Job matching using semantic similarity
- FastAPI backend
- React frontend
- Job recommendations with explanations
- Apply link integration

---

## Tech Stack

### Backend
- Python
- FastAPI
- Sentence Transformers
- Scikit-learn
- Groq API

### Frontend
- React.js
- Vite

---

## Project Structure

```bash
Agents/
Modules/
Frontend/
Resumes/
```

---

## How to Run

### Backend

```bash
cd Modules
python -m uvicorn api:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd Frontend
npm install
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

## API Endpoints

### Parse Resume

```http
POST /parse-resume
```

### Match Jobs

```http
POST /match-jobs
```

---

## Future Improvements

- Authentication system
- Better AI ranking
- Resume scoring
- Job filtering
- Deployment on cloud

---

## Team Members

Aman Pounikar
Akshat Rathor

GitHub:
https://github.com/AmanPounikar


## Project Screenshots
fig.1 (Resume upload interface)
<img width="635" height="303" alt="1" src="https://github.com/user-attachments/assets/87cfa1ec-6eea-472e-8c4b-3a419ff8ffb8" />

fig.2 (Resume Parsing and loading state)
<img width="635" height="250" alt="2" src="https://github.com/user-attachments/assets/a4f19ffa-80a4-4adb-8528-66fd62740038" />

fig.3 (Role detection interface)
<img width="635" height="382" alt="3" src="https://github.com/user-attachments/assets/929b7234-96b8-4463-abe3-618ff0fd8cd6" />

fig.4 (Input field section)
<img width="635" height="382" alt="3" src="https://github.com/user-attachments/assets/824e1e54-c07b-4c5e-8804-385f51f3db24" />

fig.5 (Job Recommendation Results)
<img width="635" height="565" alt="5" src="https://github.com/user-attachments/assets/b43eec1b-36df-46d0-921d-0576dcf889aa" />
