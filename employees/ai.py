# In Ai.py - A corrected version

import requests
from django.conf import settings

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
HEADERS = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}

def analyze_resume(resume_text, job_description): # Removed default value
    if not settings.HUGGINGFACE_API_KEY:
        # It's better to raise an error than return a string
        raise ValueError("Missing Hugging Face API key. Please add it to settings.py")

    payload = {
        "inputs": {
            "source_sentence": job_description,
            "sentences": [resume_text]
        }
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Error connecting to Hugging Face: {e}")

    if isinstance(result, dict) and "error" in result:
        raise ValueError(f"API Error: {result['error']}")

    score = result[0] if isinstance(result, list) else 0
    percentage = round(score * 100) # Use a whole number for score

    # --- THIS IS THE KEY CHANGE ---
    # Return a dictionary that matches the keys in your HTML template
    return {
        "score": percentage,
        "summary": f"The resume has a semantic similarity score of {percentage}% compared to the job description. This score reflects keyword and contextual alignment.",
        "strengths": [], # Return empty lists so the template doesn't break
        "weaknesses": [],
        "interview_questions": []
    }