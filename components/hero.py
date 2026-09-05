import streamlit as st

from components.brand import BRAND_MARK_SVG


def show_hero():
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-brand-row">
                {BRAND_MARK_SVG}
                <div>
                    <h1>ResumeIQ</h1>
                    <div class="hero-tagline">Smarter Resumes. Brighter Opportunities.</div>
                </div>
            </div>
            <div class="hero-text">
                Analyze your resume against any job description with AI --
                get an ATS score breakdown, skill-gap analysis, recruiter-style
                insights, rewrite suggestions, and a tailored cover letter.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
