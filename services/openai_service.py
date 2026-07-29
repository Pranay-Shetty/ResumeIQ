import json

from pydantic import ValidationError

from models.analysis_model import ResumeAnalysis
from services.ai_client import (
    MODEL_NAME,
    call_model_with_fallback,
    extract_json,
    has_api_key,
)

PROMPT_TEMPLATE = """You are an expert ATS recruiter.

Analyze the resume against the job description.

Respond with ONLY a single JSON object and nothing else -- no
explanations, no commentary, no Markdown code fences, no text
before or after the JSON.

Exact schema (all fields required):

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


def analyze_resume(resume_text, job_description):
    """
    Calls the AI model and returns a (ResumeAnalysis | None, error_message | None)
    tuple. On success, error_message is None. On failure, analysis is None and
    error_message explains what went wrong so the UI can show something useful
    instead of a generic "invalid response".
    """

    if not has_api_key():
        return None, (
            "OPENROUTER_API_KEY is not set. Add it to your .env file "
            "(OPENROUTER_API_KEY=sk-or-...) and restart the app."
        )

    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        job_description=job_description,
    )

    result = None

    try:
        response = call_model_with_fallback(prompt)
        result = response.choices[0].message.content.strip()
        data = extract_json(result)

        return ResumeAnalysis(**data), None

    except json.JSONDecodeError as e:
        print("❌ JSON Decode Error")
        print(result)
        print(e)
        return None, (
            "The AI model returned a response that wasn't valid JSON, "
            "even after retrying. Check the terminal for the raw response, "
            "or try again -- some models are inconsistent about following "
            "JSON-only instructions."
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
