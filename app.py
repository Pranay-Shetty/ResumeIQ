import os

import streamlit as st
from dotenv import load_dotenv

# ==========================
# Components
# ==========================
from components.sidebar import show_sidebar
from components.footer import show_footer
from components.hero import show_hero
from components.upload_panel import render_upload_panel

# =========================
# Pages
# =========================
from pages.analysis_tab import render_analysis_tab
from pages.ai_tab import render_ai_tab
from pages.resume_preview_tab import render_resume_tab
from pages.report_tab import render_report_tab

# =====================================
# Services
# =====================================
from services.resume_analyzer import analyze_resume_file

load_dotenv()

# =====================================
# Page Config
# =====================================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    with open("assets/styles.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


# =====================================
# Session State
# =====================================
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

# =====================================
# Page
# =====================================
load_css()
show_hero()
show_sidebar(api_key_missing=not bool(os.getenv("OPENROUTER_API_KEY")))

# =====================================
# Upload Section
# =====================================
uploaded_resume, job_description, analyze_clicked = render_upload_panel()

# =====================================
# Analyze Button
# =====================================
if analyze_clicked:

    if uploaded_resume is None:
        st.error("Please upload a resume.")
        st.stop()

    if not job_description.strip():
        st.error("Please paste a job description.")
        st.stop()

    with st.spinner("Analyzing your resume..."):
        try:
            analyze_resume_file(uploaded_resume, job_description)
        except Exception as e:
            st.error(f"Something went wrong while analyzing your resume: {e}")
            st.stop()

    st.rerun()

# =====================================
# Results Tabs
# =====================================
if st.session_state.analysis_complete:

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analysis",
        "🤖 AI Insights",
        "📄 Resume Preview",
        "📥 Report",
    ])

    with tab1:
        render_analysis_tab(
            st.session_state.ats_score,
            st.session_state.skill_match_percentage,
            st.session_state.matched,
            st.session_state.missing,
        )

    with tab2:
        render_ai_tab(st.session_state.analysis)

    with tab3:
        render_resume_tab(st.session_state.resume_text)

    with tab4:
        render_report_tab(
            st.session_state.ats_score,
            st.session_state.skill_match_percentage,
            st.session_state.matched,
            st.session_state.missing,
            st.session_state.analysis,
        )

    st.write("")

    if st.button("🔄 Analyze Another Resume"):
        for key in (
            "analysis_complete",
            "resume_text",
            "matched",
            "missing",
            "ats_score",
            "skill_match_percentage",
            "analysis",
        ):
            st.session_state.pop(key, None)

        st.rerun()

# =====================================
# Footer
# =====================================
show_footer()
