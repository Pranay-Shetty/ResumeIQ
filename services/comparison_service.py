from parser.pdf_parser import extract_pdf_text
from parser.docx_parser import extract_docx_text

from utils.text_cleaner import clean_text
from utils.skills import extract_skills

from services.skill_matcher import compare_skills
from services.ats_scorer import calculate_ats_score_breakdown
from services.semantic_matcher import calculate_content_similarity


def compare_resumes(uploaded_resumes, job_description):
    """
    Runs the rule-based (non-AI) scoring pipeline against every
    uploaded resume for the same job description, and returns a list
    of result dicts sorted by ATS score (highest first).

    Deliberately skips the AI-powered analysis / interview-prep /
    rewrite calls used in the single-resume flow -- running those for
    every resume in a batch would multiply API cost and latency for a
    feature whose whole point is a fast side-by-side comparison.
    """
    jd_skills = extract_skills(job_description)
    results = []

    for uploaded_resume in uploaded_resumes:
        extension = uploaded_resume.name.split(".")[-1].lower()

        if extension == "pdf":
            resume_text = extract_pdf_text(uploaded_resume)
        elif extension == "docx":
            resume_text = extract_docx_text(uploaded_resume)
        else:
            continue

        resume_text = clean_text(resume_text)
        resume_skills = extract_skills(resume_text)

        matched, missing = compare_skills(resume_skills, jd_skills)

        total = len(jd_skills)
        skill_match_percentage = round(len(matched) / total * 100) if total else 0

        breakdown = calculate_ats_score_breakdown(resume_text, matched, jd_skills)
        ats_score = round(sum(category["score"] for category in breakdown.values()))

        content_similarity = calculate_content_similarity(resume_text, job_description)

        results.append({
            "filename": uploaded_resume.name,
            "ats_score": ats_score,
            "skill_match_percentage": skill_match_percentage,
            "content_similarity": content_similarity,
            "matched_count": len(matched),
            "missing_count": len(missing),
            "missing": missing,
        })

    results.sort(key=lambda r: r["ats_score"], reverse=True)

    return results
