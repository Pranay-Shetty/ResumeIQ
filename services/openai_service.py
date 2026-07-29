import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from models.analysis_model import ResumeAnalysis

load_dotenv()


MODEL_NAME = "google/gemini-2.5-flash-lite"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "AI Resume Analyzer",
    },
)


def analyze_resume(resume_text, job_description):
    """
    Calls the AI model and returns a (ResumeAnalysis | None, error_message | None)
    tuple. On success, error_message is None. On failure, analysis is None and
    error_message explains what went wrong so the UI can show something useful
    instead of a generic "invalid response".
    """

    if not os.getenv("OPENROUTER_API_KEY"):
        return None, (
            "OPENROUTER_API_KEY is not set. Add it to your .env file "
            "(OPENROUTER_API_KEY=sk-or-...) and restart the app."
        )

    prompt = f"""
You are an expert ATS recruiter.

Analyze the resume against the job description.

Return ONLY valid JSON.

Schema:

{{
    "ats_score": 0,
    "strengths": [],
    "weaknesses": [],
    "missing_skills": [],
    "suggestions": [],
    "professional_summary": ""
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    result = None

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        result = response.choices[0].message.content.strip()

        # Remove Markdown code fences if present
        result = re.sub(r"^```json\s*", "", result)
        result = re.sub(r"^```\s*", "", result)
        result = re.sub(r"\s*```$", "", result)

        data = json.loads(result)

        return ResumeAnalysis(**data), None

    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error")
        print(result)
        print(e)
        return None, (
            "The AI model returned a response that wasn't valid JSON. "
            "This can happen with certain models -- try again, or check "
            "the terminal for the raw response."
        )

    except ValidationError as e:
        print("❌ Response Validation Error")
        print(result)
        print(e)
        return None, (
            "The AI model's response didn't match the expected fields "
            "(ats_score, strengths, weaknesses, missing_skills, "
            "suggestions, professional_summary)."
        )

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None, (
            f"The AI request failed: {e}. This is often an invalid/expired "
            "OPENROUTER_API_KEY, insufficient OpenRouter credits, or the "
            f"model '{MODEL_NAME}' being unavailable for your account."
        )
