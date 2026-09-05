import json

import openai

from pydantic import ValidationError

from models.cover_letter_model import CoverLetter
from services.ai_client import (
    MODEL_NAME,
    call_model_with_fallback,
    extract_json,
    has_api_key,
)

PROMPT_TEMPLATE = """You are an expert career coach writing a cover
letter on behalf of a job candidate.

Write a complete, ready-to-send cover letter (3-4 paragraphs) for the
candidate below, tailored specifically to the job description. Use a
{tone} tone. Reference specific, relevant experience from the resume
-- do not invent facts that aren't supported by the resume. Do not
include a physical mailing address header; start directly with a
greeting such as "Dear Hiring Manager,".

Respond with ONLY a single JSON object and nothing else -- no
explanations, no commentary, no Markdown code fences, no text before
or after the JSON.

Exact schema (all fields required):

{{
    "cover_letter": "the full cover letter text, with paragraphs separated by blank lines"
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""


def generate_cover_letter(resume_text, job_description, tone="Professional"):
    """
    Calls the AI model to draft a tailored cover letter. Returns a
    (CoverLetter | None, error_message | None) tuple, mirroring
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
        tone=tone,
    )

    result = None

    try:
        response = call_model_with_fallback(prompt)
        result = response.choices[0].message.content.strip()
        data = extract_json(result)

        return CoverLetter(**data), None

    except json.JSONDecodeError as e:
        print("❌ Cover Letter JSON Decode Error")
        print(result)
        print(e)
        return None, (
            "The AI model returned a response that wasn't valid JSON, "
            "even after retrying. Try again, or check the terminal for "
            "the raw response."
        )

    except ValidationError as e:
        print("❌ Cover Letter Response Validation Error")
        print(result)
        print(e)
        return None, (
            "The AI model's response didn't match the expected field "
            "(cover_letter)."
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
        print(f"❌ Cover Letter Unexpected Error: {e}")
        return None, (
            f"The AI request failed: {e}. This is often an invalid/expired "
            "OPENROUTER_API_KEY, insufficient OpenRouter credits, or the "
            f"model '{MODEL_NAME}' being unavailable for your account."
        )
