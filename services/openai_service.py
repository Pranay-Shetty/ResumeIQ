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


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _extract_json(raw_text: str) -> dict:
    """
    Parse a JSON object out of a model response. Models sometimes wrap
    the JSON in code fences or add a stray sentence before/after it
    despite instructions not to -- try a direct parse first, then fall
    back to extracting the outermost {...} substring.
    """
    text = _strip_code_fences(raw_text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise json.JSONDecodeError("No JSON object found in response", text, 0)

    return json.loads(text[start:end + 1])


def _call_model(prompt: str, use_json_mode: bool):
    kwargs = dict(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    if use_json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    return client.chat.completions.create(**kwargs)


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

    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        job_description=job_description,
    )

    result = None

    try:
        # Prefer strict JSON mode when the model/provider supports it --
        # fall back to a plain completion if the parameter is rejected.
        try:
            response = _call_model(prompt, use_json_mode=True)
        except Exception as json_mode_error:
            print(f"⚠ JSON mode unavailable, falling back to plain completion: {json_mode_error}")
            response = _call_model(prompt, use_json_mode=False)

        result = response.choices[0].message.content.strip()

        data = _extract_json(result)

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
