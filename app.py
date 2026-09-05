import os

import streamlit as st
from dotenv import load_dotenv

# ==========================
# Components
# ==========================
from components.sidebar import show_sidebar
from components.footer import show_footer
from components.hero import show_hero
from components.feature_grid import show_feature_highlights
from components.upload_panel import render_upload_panel

# =========================
# Result Sections
# =========================
# NOTE: this folder is intentionally named "sections" and NOT "pages" --
# Streamlit auto-detects any folder literally named "pages/" and turns
# every .py file inside it into a clickable multipage-app nav entry in
# the sidebar. These files only define render_*() functions and were
# never meant to be standalone pages, so that auto-nav just produced
# broken/dead links cluttering the sidebar.
from sections.analysis_tab import render_analysis_tab
from sections.ai_tab import render_ai_tab
from sections.rewrite_tab import render_rewrite_tab
from sections.interview_prep_tab import render_interview_prep_tab
from sections.cover_letter_tab import render_cover_letter_tab
from sections.resume_preview_tab import render_resume_tab
from sections.report_tab import render_report_tab
from sections.compare_tab import render_compare_section
from sections.history_tab import render_history_section

# =====================================
# Services
# =====================================
from services.resume_analyzer import analyze_resume_file
from services.history_service import add_to_history

load_dotenv()

# =====================================
# Page Config
# =====================================
st.set_page_config(
    page_title="ResumeIQ",
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
# Session State Defaults
# =====================================
_DEFAULTS = {
    "analysis_complete": False,
    "upload_reset_key": 0,
    "show_summary_dialog": False,
}

for _key, _value in _DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _value

RESULT_KEYS = (
    "resume_text",
    "job_description",
    "matched",
    "missing",
    "ats_score",
    "ats_breakdown",
    "content_similarity",
    "skill_match_percentage",
    "analysis",
    "ai_error",
    "interview_prep",
    "interview_prep_error",
    "rewrite",
    "rewrite_error",
    "uploaded_resume_name",
)

# On-demand extras that shouldn't carry over to a newly-analyzed resume.
_RESET_EXTRA_KEYS = ("cover_letter", "cover_letter_error")


def reset_analysis():
    for key in RESULT_KEYS + _RESET_EXTRA_KEYS + ("analysis_complete", "show_summary_dialog"):
        st.session_state.pop(key, None)
    st.session_state.upload_reset_key += 1


# =====================================
# Results Summary Dialog
# =====================================
@st.dialog("Analysis Complete")
def show_results_summary():
    col1, col2 = st.columns(2)

    with col1:
        st.metric("ATS Score", f"{st.session_state.ats_score}%")

    with col2:
        st.metric("Skill Match", f"{st.session_state.skill_match_percentage}%")

    missing = st.session_state.get("missing") or []

    st.write("")

    if missing:
        preview = ", ".join(missing[:5])
        if len(missing) > 5:
            preview += f", +{len(missing) - 5} more"
        st.warning(f"**Top missing skills:** {preview}")
    else:
        st.success("No missing skills detected against this job description")

    if st.session_state.get("interview_prep") is not None:
        st.info(
            f"{len(st.session_state.interview_prep.questions)} tailored "
            "interview questions are ready in the Interview Prep tab."
        )

    if st.session_state.get("rewrite") is not None and st.session_state.rewrite.rewrites:
        st.info(
            f"{len(st.session_state.rewrite.rewrites)} rewrite suggestions "
            "are ready in the Rewrite Suggestions tab."
        )

    st.write("")

    if st.button("View Full Analysis →", use_container_width=True, type="primary"):
        st.session_state.show_summary_dialog = False
        st.rerun()


# =====================================
# Page
# =====================================
load_css()
show_hero()
app_mode = show_sidebar(
    api_key_missing=not bool(os.getenv("OPENROUTER_API_KEY")),
    ats_score=st.session_state.get("ats_score") if st.session_state.analysis_complete else None,
    skill_match_percentage=st.session_state.get("skill_match_percentage") if st.session_state.analysis_complete else None,
)

# =====================================
# Compare Mode
# =====================================
if app_mode == "compare":
    render_compare_section()
    show_footer()
    st.stop()

if app_mode == "history":
    render_history_section()
    show_footer()
    st.stop()

# =====================================
# Upload Section
# =====================================
# Once an analysis exists, collapse the big upload/JD panel into a
# slim status bar so the results tabs sit near the top of the page
# instead of requiring a scroll past the full upload UI.
if not st.session_state.analysis_complete:
    show_feature_highlights()

    uploaded_resume, job_description, analyze_clicked = render_upload_panel(
        reset_key=st.session_state.upload_reset_key
    )
else:
    uploaded_resume, job_description, analyze_clicked = None, None, False

    with st.container(border=True):
        status_col, action_col = st.columns([4, 1])

        with status_col:
            st.markdown(
                f"**Analyzed:** {st.session_state.get('uploaded_resume_name', 'your resume')}"
            )

        with action_col:
            if st.button("New Resume", use_container_width=True):
                reset_analysis()
                st.rerun()

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

    with st.status("Starting analysis...", expanded=True) as status:
        try:
            analyze_resume_file(
                uploaded_resume,
                job_description,
                progress_callback=lambda message: status.write(message),
            )
        except Exception as e:
            status.update(label="Analysis failed", state="error")
            st.error(f"Something went wrong while analyzing your resume: {e}")
            st.stop()

        status.update(label="Analysis complete", state="complete")

    add_to_history()
    st.session_state.show_summary_dialog = True
    st.rerun()

# =====================================
# Results
# =====================================
if st.session_state.analysis_complete:

    if st.session_state.show_summary_dialog:
        show_results_summary()

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Analysis",
        "AI Insights",
        "Rewrite Suggestions",
        "Interview Prep",
        "Cover Letter",
        "Resume Preview",
        "Report",
    ])

    with tab1:
        render_analysis_tab(
            st.session_state.ats_score,
            st.session_state.skill_match_percentage,
            st.session_state.matched,
            st.session_state.missing,
            st.session_state.get("ats_breakdown"),
            st.session_state.get("content_similarity"),
        )

    with tab2:
        render_ai_tab(
            st.session_state.analysis,
            st.session_state.get("ai_error"),
        )

    with tab3:
        render_rewrite_tab(
            st.session_state.get("rewrite"),
            st.session_state.get("rewrite_error"),
        )

    with tab4:
        render_interview_prep_tab(
            st.session_state.interview_prep,
            st.session_state.get("interview_prep_error"),
        )

    with tab5:
        render_cover_letter_tab(
            st.session_state.resume_text,
            st.session_state.get("job_description", ""),
        )

    with tab6:
        render_resume_tab(st.session_state.resume_text)

    with tab7:
        render_report_tab(
            st.session_state.ats_score,
            st.session_state.skill_match_percentage,
            st.session_state.matched,
            st.session_state.missing,
            st.session_state.analysis,
            st.session_state.interview_prep,
            st.session_state.get("ats_breakdown"),
            st.session_state.get("content_similarity"),
            st.session_state.get("rewrite"),
        )

# =====================================
# Footer
# =====================================
show_footer()
