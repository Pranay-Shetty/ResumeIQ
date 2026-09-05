import json

import openai

from pydantic import ValidationError

from models.interview_prep_model import InterviewPrep
from services.ai_client import (
    MODEL_NAME,
    call_model_with_fallback,
    extract_json,
    has_api_key,
)

PROMPT_TEMPLATE = """You are an expert technical interviewer and career coach.

Based on the job description and candidate resume below, generate a
realistic interview preparation kit tailored specifically to this role.

Respond with ONLY a single JSON object and nothing else -- no
explanations, no commentary, no Markdown code fences, no text before
or after the JSON.

Exact schema (all fields required):

{{
    "questions": [
        {{
            "category": "Behavioral | Technical | Situational | Role-Specific",
            "question": "...",
            "suggested_answer": "A concise, tailored example answer (2-4 sentences) that draws on the candidate's actual resume where relevant."
        }}
    ],
    "tips": ["..."]
}}

Generate exactly 8 questions spanning a mix of the categories above,
relevant specifically to this job description -- not generic
interview questions. Base the suggested answers on the candidate's
real resume content wherever possible. Also include 3-5 short,
practical general_tips for interviewing for this specific role.

Job Description:
{job_description}

Candidate Resume:
{resume_text}
"""


def generate_interview_prep(resume_text, job_description):
    """
    Calls the AI model to generate interview questions + suggested
    answers tailored to the job description and resume. Returns a
    (InterviewPrep | None, error_message | None) tuple, mirroring
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

        return InterviewPrep(**data), None

    except json.JSONDecodeError as e:
        print("❌ Interview Prep JSON Decode Error")
        print(result)
        print(e)
        return None, (
            "The AI model returned a response that wasn't valid JSON, "
            "even after retrying. Try again, or check the terminal for "
            "the raw response."
        )

    except ValidationError as e:
        print("❌ Interview Prep Response Validation Error")
        print(result)
        print(e)
        return None, (
            "The AI model's response didn't match the expected fields "
            "(questions[].category/question/suggested_answer, tips)."
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
        print(f"❌ Interview Prep Unexpected Error: {e}")
        return None, (
            f"The AI request failed: {e}. This is often an invalid/expired "
            "OPENROUTER_API_KEY, insufficient OpenRouter credits, or the "
            f"model '{MODEL_NAME}' being unavailable for your account."
        )
