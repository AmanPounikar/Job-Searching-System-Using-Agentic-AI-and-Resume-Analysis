import os

# 🔥 MUST BE FIRST — before ANY imports
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_DOWNLOAD_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

import warnings
warnings.filterwarnings("ignore")

from transformers import logging
logging.set_verbosity_error()

# 🔥 EXTRA — silence huggingface hub logger
import logging as py_logging
py_logging.getLogger("huggingface_hub").setLevel(py_logging.ERROR)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessor import preprocess_text

# 🔥 load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def match_jobs(resume_text, jobs):

    clean_jobs = []

    for job in jobs:
        desc = (
            job.get("job_description") or
            job.get("job_snippet") or
            str(job.get("job_highlights")) or
            job.get("job_title") or
            ""
        )

        desc = preprocess_text(desc)

        if desc.strip():
            job["combined_text"] = desc
            clean_jobs.append(job)

    jobs = clean_jobs

    if not jobs:
        print("No jobs found.")
        return []

    job_texts = [job["combined_text"] for job in jobs]

    # 🔥 embeddings
    resume_embedding = model.encode([resume_text], convert_to_numpy=True)
    job_embeddings = model.encode(job_texts, convert_to_numpy=True)

    similarity_scores = cosine_similarity(resume_embedding, job_embeddings)

    for i, job in enumerate(jobs):
        job["match_score"] = round(float(similarity_scores[0][i]), 4)

    ranked_jobs = sorted(jobs, key=lambda x: x["match_score"], reverse=True)

    return ranked_jobs[:5]