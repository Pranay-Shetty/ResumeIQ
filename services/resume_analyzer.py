import streamlit as st

from parser.pdf_parser import extract_pdf_text
from parser.docx_parser import extract_docx_text

from utils.text_cleaner import clean_text
from utils.skills import extract_skills

from services.skill_matcher import compare_skills
from services.ats_scorer import calculate_ats_score_breakdown
from services.semantic_matcher import calculate_content_similarity
from services.openai_service import analyze_resume
from services.interview_prep_service import generate_interview_prep
from services.rewrite_service import generate_resume_rewrite


def analyze_resume_file(uploaded_resume, job_description, progress_callback=None):
    """
    Performs the complete resume analysis pipeline.
    Saves the results into Streamlit session state.

    progress_callback, if given, is called with a short human-readable
    string before each stage of the pipeline -- lets the UI show real
    step-by-step progress (via st.status) instead of one static
    spinner message for what can be a multi-second, multi-AI-call
    pipeline.
    """

    def _progress(message):
        if progress_callback:
            progress_callback(message)

    extension = uploaded_resume.name.split(".")[-1].lower()

    _progress("Extracting resume text...")

    if extension == "pdf":
        resume_text = extract_pdf_text(uploaded_resume)

    elif extension == "docx":
        resume_text = extract_docx_text(uploaded_resume)

    else:
        raise ValueError("Unsupported file format.")

    resume_text = clean_text(resume_text)

    _progress("Matching skills against the job description...")

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    matched, missing = compare_skills(
        resume_skills,
        jd_skills
    )

    total = len(jd_skills)

    if total:
        skill_match_percentage = round(
            len(matched) / total * 100
        )
    else:
        skill_match_percentage = 0

    _progress("Calculating ATS score breakdown...")

    ats_breakdown = calculate_ats_score_breakdown(
        resume_text,
        matched,
        jd_skills,
    )
    ats_score = round(sum(category["score"] for category in ats_breakdown.values()))

    _progress("Calculating content similarity...")

    content_similarity = calculate_content_similarity(
        resume_text,
        job_description,
    )

    _progress("Running AI resume analysis...")

    analysis, ai_error = analyze_resume(
        resume_text,
        job_description
    )

    _progress("Generating interview prep questions...")

    interview_prep, interview_prep_error = generate_interview_prep(
        resume_text,
        job_description,
    )

    _progress("Generating rewrite suggestions...")

    rewrite, rewrite_error = generate_resume_rewrite(
        resume_text,
        job_description,
    )

    _progress("Saving results...")

    st.session_state.resume_text = resume_text
    st.session_state.job_description = job_description
    st.session_state.matched = matched
    st.session_state.missing = missing
    st.session_state.ats_score = ats_score
    st.session_state.ats_breakdown = ats_breakdown
    st.session_state.content_similarity = content_similarity
    st.session_state.skill_match_percentage = skill_match_percentage
    st.session_state.analysis = analysis
    st.session_state.ai_error = ai_error
    st.session_state.interview_prep = interview_prep
    st.session_state.interview_prep_error = interview_prep_error
    st.session_state.rewrite = rewrite
    st.session_state.rewrite_error = rewrite_error
    st.session_state.analysis_complete = True
    st.session_state.uploaded_resume_name = uploaded_resume.name
