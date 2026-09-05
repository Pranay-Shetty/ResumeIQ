import pytest
from pydantic import ValidationError

from models.analysis_model import ResumeAnalysis
from models.interview_prep_model import InterviewPrep
from models.rewrite_model import ResumeRewrite
from models.cover_letter_model import CoverLetter


def test_resume_analysis_accepts_valid_payload():
    analysis = ResumeAnalysis(
        ats_score=80,
        strengths=["Strong Python background"],
        weaknesses=["No cloud experience"],
        missing_skills=["AWS"],
        suggestions=["Add a metrics-driven bullet point"],
        professional_summary="A solid backend engineer.",
    )
    assert analysis.ats_score == 80


def test_resume_analysis_rejects_missing_fields():
    with pytest.raises(ValidationError):
        ResumeAnalysis(ats_score=80)


def test_interview_prep_accepts_valid_payload():
    prep = InterviewPrep(
        questions=[
            {
                "category": "Behavioral",
                "question": "Tell me about a challenge you faced.",
                "suggested_answer": "I once had to debug a production incident...",
            }
        ],
        tips=["Research the company beforehand."],
    )
    assert len(prep.questions) == 1
    assert prep.questions[0].category == "Behavioral"


def test_resume_rewrite_accepts_valid_payload():
    rewrite = ResumeRewrite(
        rewrites=[
            {
                "original": "Responsible for the database",
                "improved": "Owned and optimized a PostgreSQL database serving 1M+ daily queries",
                "reason": "Adds scope and a measurable metric",
            }
        ],
        general_advice=["Lead every bullet with a strong action verb."],
    )
    assert rewrite.rewrites[0].original == "Responsible for the database"


def test_cover_letter_accepts_valid_payload():
    letter = CoverLetter(cover_letter="Dear Hiring Manager, ...")
    assert letter.cover_letter.startswith("Dear")


def test_cover_letter_rejects_missing_field():
    with pytest.raises(ValidationError):
        CoverLetter()
