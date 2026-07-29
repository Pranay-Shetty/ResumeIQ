import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

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


def has_api_key() -> bool:
    return bool(os.getenv("OPENROUTER_API_KEY"))


def call_model(prompt: str, use_json_mode: bool = True):
    """
    Calls the shared model. use_json_mode requests strict JSON output
    where the provider supports it -- callers should catch failures
    here and retry with use_json_mode=False as a fallback.
    """
    kwargs = dict(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    if use_json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    return client.chat.completions.create(**kwargs)


def call_model_with_fallback(prompt: str):
    """
    Tries strict JSON mode first, falling back to a plain completion
    if the model/provider rejects the response_format parameter.
    """
    try:
        return call_model(prompt, use_json_mode=True)
    except Exception as json_mode_error:
        print(f"⚠ JSON mode unavailable, falling back to plain completion: {json_mode_error}")
        return call_model(prompt, use_json_mode=False)


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def extract_json(raw_text: str) -> dict:
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
