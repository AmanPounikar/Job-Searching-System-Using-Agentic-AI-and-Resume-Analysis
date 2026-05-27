import { useState, useRef } from "react";

const API = "http://127.0.0.1:8000";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: #f5f3ee;
    min-height: 100vh;
    color: #1a1a1a;
  }

  .app {
    max-width: 780px;
    margin: 0 auto;
    padding: 3rem 1.5rem 5rem;
  }

  /* ── Hero ── */
  .hero { margin-bottom: 3rem; }

  .hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a7a3a;
    background: #e4edda;
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 1.25rem;
  }

  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.4rem);
    font-weight: 800;
    line-height: 1.05;
    color: #111;
    margin-bottom: 1rem;
  }

  .hero-title em {
    font-style: normal;
    color: #6a9a3f;
    position: relative;
  }

  .hero-sub {
    font-size: 1.05rem;
    color: #666;
    font-weight: 300;
    max-width: 420px;
    line-height: 1.7;
  }

  /* ── Card ── */
  .card {
    background: #fff;
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.25rem;
    border: 1px solid #e8e4dc;
  }

  .card-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #999;
    margin-bottom: 1rem;
  }

  /* ── Upload ── */
  .upload-zone {
    border: 2px dashed #d4cfc6;
    border-radius: 14px;
    padding: 3rem 2rem;
    text-align: center;
    cursor: pointer;
    position: relative;
    transition: border-color 0.2s, background 0.2s;
  }

  .upload-zone:hover, .upload-zone.drag {
    border-color: #6a9a3f;
    background: #f4f9ee;
  }

  .upload-zone input {
    position: absolute; inset: 0; opacity: 0; cursor: pointer;
  }

  .upload-icon {
    font-size: 2.8rem;
    margin-bottom: 0.75rem;
    display: block;
  }

  .upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 0.3rem;
  }

  .upload-hint { font-size: 0.85rem; color: #aaa; }

  .upload-success {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #eaf3e0;
    border-radius: 10px;
    padding: 10px 16px;
    margin-top: 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: #3d6e20;
  }

  /* ── Detected role ── */
  .role-detect {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #f8f6f1;
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 1.25rem;
    border: 1px solid #ede9e0;
  }

  .role-detect-label { font-size: 11px; color: #aaa; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
  .role-detect-value { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700; color: #3d6e20; }

  /* ── Fields ── */
  .field { margin-bottom: 1rem; }

  .field label {
    display: block;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    color: #aaa;
    margin-bottom: 6px;
  }

  .field input {
    width: 100%;
    padding: 11px 16px;
    border-radius: 10px;
    border: 1px solid #e0dbd0;
    background: #faf9f6;
    color: #111;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.97rem;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .field input:focus {
    border-color: #6a9a3f;
    box-shadow: 0 0 0 3px #6a9a3f22;
    background: #fff;
  }

  .field-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }

  /* ── Button ── */
  .btn-find {
    width: 100%;
    padding: 15px;
    border-radius: 12px;
    background: #1a1a1a;
    color: #fff;
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    border: none;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s;
    letter-spacing: 0.02em;
    margin-top: 0.5rem;
  }

  .btn-find:hover { background: #3d6e20; transform: translateY(-2px); }
  .btn-find:active { transform: scale(0.98); }
  .btn-find:disabled { background: #ccc; cursor: not-allowed; transform: none; }

  /* ── Loading ── */
  .loading-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1rem;
    gap: 1rem;
  }

  .loading-dots { display: flex; gap: 6px; }

  .loading-dots span {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #6a9a3f;
    animation: bounce 1.2s infinite;
  }

  .loading-dots span:nth-child(2) { animation-delay: 0.2s; }
  .loading-dots span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes bounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40% { transform: scale(1); opacity: 1; }
  }

  .loading-text { font-size: 0.9rem; color: #999; font-weight: 300; }

  /* ── Results ── */
  .results-header {
    display: flex;
    align-items: baseline;
    gap: 10px;
    margin-bottom: 1.25rem;
  }

  .results-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    color: #111;
  }

  .results-pill {
    font-size: 0.78rem;
    font-weight: 600;
    background: #e4edda;
    color: #3d6e20;
    border-radius: 999px;
    padding: 3px 12px;
  }

  /* ── Job card ── */
  .job-card {
    background: #fff;
    border: 1px solid #e8e4dc;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    animation: fadeUp 0.4s ease both;
  }

  .job-card:hover {
    border-color: #6a9a3f;
    transform: translateY(-3px);
    box-shadow: 0 8px 24px #6a9a3f18;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .job-card:nth-child(2) { animation-delay: 0.07s; }
  .job-card:nth-child(3) { animation-delay: 0.14s; }
  .job-card:nth-child(4) { animation-delay: 0.21s; }
  .job-card:nth-child(5) { animation-delay: 0.28s; }

  .job-top {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .job-rank {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 800;
    color: #6a9a3f;
    background: #eaf3df;
    border-radius: 8px;
    padding: 5px 10px;
    flex-shrink: 0;
    margin-top: 3px;
  }

  .job-info { flex: 1; }

  .job-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #111;
    margin-bottom: 3px;
  }

  .job-company { font-size: 0.875rem; color: #888; font-weight: 300; }

  .score-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
  }

  .score-label { font-size: 11px; color: #aaa; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }

  .score-bar-wrap {
    flex: 1;
    height: 5px;
    background: #f0ede6;
    border-radius: 999px;
    overflow: hidden;
  }

  .score-bar {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #6a9a3f, #a8c97a);
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .score-pct {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #3d6e20;
    min-width: 38px;
    text-align: right;
  }

  .job-explain {
    font-size: 0.875rem;
    color: #666;
    line-height: 1.6;
    background: #f8f6f1;
    border-radius: 10px;
    padding: 10px 14px;
    border-left: 3px solid #a8c97a;
    font-weight: 300;
  }

  .job-apply {
    display: inline-block;
    margin-top: 12px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #6a9a3f;
    text-decoration: none;
    border: 1px solid #c8dfb0;
    border-radius: 8px;
    padding: 5px 14px;
    transition: background 0.15s;
  }

  .job-apply:hover { background: #eaf3df; }

  /* ── Error ── */
  .error-box {
    background: #fff5f5;
    border: 1px solid #ffd0d0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: #c0392b;
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }
`;

export default function App() {
  const [file, setFile] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [role, setRole] = useState("");
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [jobs, setJobs] = useState([]);
  const [step, setStep] = useState("upload"); // upload | form | loading | results
  const [error, setError] = useState("");
  const [drag, setDrag] = useState(false);
  const resultsRef = useRef(null);

  async function handleFile(f) {
    if (!f || f.type !== "application/pdf") return;
    setFile(f);
    setError("");
    setStep("parsing");

    const fd = new FormData();
    fd.append("file", f);

    try {
      const res = await fetch(`${API}/parse-resume`, { method: "POST", body: fd });
      const data = await res.json();
      setResumeData(data);
      setRole(data.detected_role || "");
      setStep("form");
    } catch {
      setError("Could not connect to the backend. Make sure api.py is running.");
      setStep("upload");
    }
  }

  async function findJobs() {
    if (!role.trim()) return;
    setStep("loading");
    setError("");

    const fd = new FormData();
    fd.append("resume_text", resumeData.resume_text);
    fd.append("clean_text", resumeData.clean_text);
    fd.append("role", role);
    fd.append("country", country);
    fd.append("city", city);

    try {
      const res = await fetch(`${API}/match-jobs`, { method: "POST", body: fd });
      const data = await res.json();
      if (!data.jobs?.length) {
        setError("No jobs found. Try a different role or location.");
        setStep("form");
        return;
      }
      setJobs(data.jobs);
      setStep("results");
      setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
    } catch {
      setError("Something went wrong fetching jobs.");
      setStep("form");
    }
  }

  return (
    <>
      <style>{styles}</style>
      <div className="app">

        {/* Hero */}
        <div className="hero">
          <div className="hero-eyebrow">✦ AI-Powered</div>
          <h1 className="hero-title">Jobs that actually<br /><em>fit you.</em></h1>
          <p className="hero-sub">Upload your resume, let AI detect your role, and get matched to the best jobs out there.</p>
        </div>

        {/* Upload */}
        <div className="card">
          <p className="card-label">Step 1 — Your Resume</p>
          <div
            className={`upload-zone${drag ? " drag" : ""}`}
            onDragOver={e => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            onDrop={e => { e.preventDefault(); setDrag(false); handleFile(e.dataTransfer.files[0]); }}
          >
            <input type="file" accept=".pdf" onChange={e => handleFile(e.target.files[0])} />
            <span className="upload-icon">📄</span>
            <div className="upload-title">Drop your PDF here or click to browse</div>
            <div className="upload-hint">Only PDF resumes are supported</div>
          </div>

          {step === "parsing" && (
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: "1rem", color: "#999", fontSize: "0.9rem" }}>
              <div className="loading-dots"><span /><span /><span /></div>
              Parsing resume...
            </div>
          )}

          {file && step !== "parsing" && (
            <div className="upload-success">
              <span>✅</span> {file.name}
            </div>
          )}
        </div>

        {/* Form */}
        {(step === "form" || step === "loading" || step === "results") && (
          <div className="card">
            <p className="card-label">Step 2 — Confirm & Search</p>

            {resumeData?.detected_role && (
              <div className="role-detect">
                <span className="role-detect-label">Detected role</span>
                <span className="role-detect-value">{resumeData.detected_role}</span>
              </div>
            )}

            <div className="field">
              <label>Role / Job Title</label>
              <input value={role} onChange={e => setRole(e.target.value)} placeholder="e.g. Frontend Developer" />
            </div>

            <div className="field-row">
              <div className="field">
                <label>Country</label>
                <input value={country} onChange={e => setCountry(e.target.value)} placeholder="e.g. India" />
              </div>
              <div className="field">
                <label>City (optional)</label>
                <input value={city} onChange={e => setCity(e.target.value)} placeholder="e.g. Bangalore" />
              </div>
            </div>

            {error && <div className="error-box">⚠️ {error}</div>}

            <button className="btn-find" onClick={findJobs} disabled={step === "loading"}>
              {step === "loading" ? "Finding matches..." : "Find matching jobs →"}
            </button>
          </div>
        )}

        {/* Loading */}
        {step === "loading" && (
          <div className="loading-wrap">
            <div className="loading-dots"><span /><span /><span /></div>
            <p className="loading-text">Scanning jobs and ranking matches for you…</p>
          </div>
        )}

        {/* Results */}
        {step === "results" && (
          <div ref={resultsRef}>
            <div className="results-header">
              <span className="results-title">Top matches</span>
              <span className="results-pill">{jobs.length} jobs found</span>
            </div>

            {jobs.map((job, i) => {
              const pct = Math.round(job.match_score * 100);
              return (
                <div className="job-card" key={i}>
                  <div className="job-top">
                    <div className="job-rank">#{i + 1}</div>
                    <div className="job-info">
                      <div className="job-title">{job.job_title}</div>
                      <div className="job-company">{job.employer_name}</div>
                    </div>
                  </div>

                  <div className="score-row">
                    <span className="score-label">Match</span>
                    <div className="score-bar-wrap">
                      <div className="score-bar" style={{ width: `${pct}%` }} />
                    </div>
                    <span className="score-pct">{pct}%</span>
                  </div>

                  <div className="job-explain">{job.explanation}</div>

                  {job.job_apply_link && (
                    <a className="job-apply" href={job.job_apply_link} target="_blank" rel="noreferrer">
                      Apply now ↗
                    </a>
                  )}
                </div>
              );
            })}
          </div>
        )}

      </div>
    </>
  );
}
