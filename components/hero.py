import streamlit as st


def show_hero():
    st.markdown(
        """
        <div class="hero">
            <h1>ResumeIQ</h1>
            <div class="hero-text">
                Analyze your resume against any job description with AI --
                get an ATS score breakdown, skill-gap analysis, recruiter-style
                insights, rewrite suggestions, and a tailored cover letter.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
