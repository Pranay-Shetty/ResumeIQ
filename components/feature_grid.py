import streamlit as st

FEATURES = [
    ("🎯", "ATS Score Breakdown", "See exactly why your resume scored what it did, broken down by keyword match, achievements, length, and contact info."),
    ("🤖", "AI Resume Analysis", "Get recruiter-style strengths, weaknesses, and a tailored professional summary."),
    ("✍️", "Rewrite Suggestions", "Weak resume lines rewritten to be stronger and tailored to the job description, with the reasoning behind each change."),
    ("🎤", "Interview Prep", "Practice with role-specific interview questions and suggested answers drawn from your own resume."),
    ("✉️", "Cover Letter Generator", "Generate a tailored, editable cover letter in the tone you choose, ready to download."),
    ("🆚", "Compare Resumes", "Score multiple resume versions against the same job description, side by side, ranked by fit."),
]


def show_feature_highlights():
    """
    A compact, always-visible showcase of what the tool can do --
    shown on the landing/upload screen so a first-time user sees the
    full feature set up front, rather than discovering it tab by tab
    only after running an analysis.
    """
    cards_html = "".join(
        f"""
        <div class="feature-card">
            <div class="feature-card-icon">{icon}</div>
            <div class="feature-card-title">{title}</div>
            <div class="feature-card-desc">{desc}</div>
        </div>
        """
        for icon, title, desc in FEATURES
    )

    st.markdown(f'<div class="feature-grid">{cards_html}</div>', unsafe_allow_html=True)
