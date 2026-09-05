import json

import openai

from pydantic import ValidationError

from models.rewrite_model import ResumeRewrite
from services.ai_client import (
    MODEL_NAME,
    call_model_with_fallback,
    extract_json,
    has_api_key,
)

PROMPT_TEMPLATE = """You are an expert resume writer and career coach.

Find the 5-8 weakest or most generic lines in the resume below
(vague responsibilities, no measurable impact, passive phrasing,
buzzwords with nothing backing them up) and rewrite each one to be
stronger and tailored to the job description -- specific, quantified
where you can reasonably suggest a placeholder metric (e.g. "reduced
processing time by an estimated X%"), and using strong action verbs.

Respond with ONLY a single JSON object and nothing else -- no
explanations, no commentary, no Markdown code fences, no text before
or after the JSON.

Exact schema (all fields required):

{{
    "rewrites": [
        {{
            "original": "the exact original line from the resume",
            "improved": "the rewritten, stronger version",
            "reason": "one short sentence on why this is stronger"
        }}
    ],
    "general_advice": ["..."]
}}

Also include 3-5 short general_advice items on resume writing style
specifically relevant to this job description, beyond the individual
rewrites.

Resume:
{resume_text}

Job Description:
{job_description}
"""


def generate_resume_rewrite(resume_text, job_description):
    """
    Calls the AI model to rewrite weak resume bullet points, tailored
    to the job description. Returns a
    (ResumeRewrite | None, error_message | None) tuple, mirroring
    services.openai_service.analyze_resume.
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

        return ResumeRewrite(**data), None

    except json.JSONDecodeError as e:
        print("❌ Rewrite JSON Decode Error")
        print(result)
        print(e)
        return None, (
            "The AI model returned a response that wasn't valid JSON, "
            "even after retrying. Try again, or check the terminal for "
            "the raw response."
        )

    except ValidationError as e:
        print("❌ Rewrite Response Validation Error")
        print(result)
        print(e)
        return None, (
            "The AI model's response didn't match the expected fields "
            "(rewrites[].original/improved/reason, general_advice)."
        )

    except openai.RateLimitError as e:
        print(f"❌ Rate Limited: {e}")
        return None, (
            "OpenRouter is rate-limiting requests right now (the client "
            "already retried automatically). Wait a moment and try again."
        )

    except (openai.APITimeoutError, openai.APIConnectionError) as e:
        print(f"❌ Network Error: {e}")
        return None, (
            "The request to OpenRouter timed out or the connection was "
            "interrupted, even after retrying. Check your network "
            "connection and try again."
        )

    except Exception as e:
        print(f"❌ Rewrite Unexpected Error: {e}")
        return None, (
            f"The AI request failed: {e}. This is often an invalid/expired "
            "OPENROUTER_API_KEY, insufficient OpenRouter credits, or the "
            f"model '{MODEL_NAME}' being unavailable for your account."
        )
