"""
These tests cover the "no API key configured" branch of every AI
service -- the one path that's safe to exercise without a live
OPENROUTER_API_KEY or a network call. Success-path behavior (actual
model calls) is not covered here; it would need a real key and either
live network access or a mocked OpenAI client.
"""

from services.openai_service import analyze_resume
from services.interview_prep_service import generate_interview_prep
from services.rewrite_service import generate_resume_rewrite
from services.cover_letter_service import generate_cover_letter
from services.ai_client import has_api_key


def _clear_api_key(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)


def test_has_api_key_false_when_unset(monkeypatch):
    _clear_api_key(monkeypatch)
    assert has_api_key() is False


def test_has_api_key_true_when_set(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test-key")
    assert has_api_key() is True


def test_analyze_resume_without_key_returns_helpful_error(monkeypatch):
    _clear_api_key(monkeypatch)
    analysis, error = analyze_resume("resume text", "job description")

    assert analysis is None
    assert "OPENROUTER_API_KEY" in error


def test_interview_prep_without_key_returns_helpful_error(monkeypatch):
    _clear_api_key(monkeypatch)
    prep, error = generate_interview_prep("resume text", "job description")

    assert prep is None
    assert "OPENROUTER_API_KEY" in error


def test_rewrite_without_key_returns_helpful_error(monkeypatch):
    _clear_api_key(monkeypatch)
    rewrite, error = generate_resume_rewrite("resume text", "job description")

    assert rewrite is None
    assert "OPENROUTER_API_KEY" in error


def test_cover_letter_without_key_returns_helpful_error(monkeypatch):
    _clear_api_key(monkeypatch)
    letter, error = generate_cover_letter("resume text", "job description")

    assert letter is None
    assert "OPENROUTER_API_KEY" in error
