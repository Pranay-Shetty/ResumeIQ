import streamlit as st

from components.brand import brand_logo_full_html


def show_hero():
    st.markdown(
        f"""
        <div class="hero">
            {brand_logo_full_html(340)}
            <div class="hero-text">
                Analyze your resume against any job description with AI --
                get an ATS score breakdown, skill-gap analysis, recruiter-style
                insights, rewrite suggestions, and a tailored cover letter.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
