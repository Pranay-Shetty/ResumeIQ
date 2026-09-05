import streamlit as st

from components.brand import BRAND_MARK_SVG


def show_sidebar(
    api_key_missing: bool = False,
    ats_score=None,
    skill_match_percentage=None,
):
    """
    Renders the sidebar and returns the selected app mode:
    "single" (analyze one resume), "compare" (score several resumes
    against the same job description side by side), or "history"
    (revisit past analyses from this session).
    """

    with st.sidebar:

        st.markdown(
            f"""
            <div class="sidebar-brand">
                {BRAND_MARK_SVG}
                <div>
                    <div class="sidebar-brand-title">ResumeIQ</div>
                    <div class="sidebar-brand-version">Version 1.2</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mode_label = st.radio(
            "Mode",
            ["Analyze One Resume", "Compare Resumes", "History"],
            key="app_mode",
            label_visibility="collapsed",
        )

        if mode_label == "Compare Resumes":
            mode = "compare"
        elif mode_label == "History":
            mode = "history"
        else:
            mode = "single"

        st.markdown("---")

        # Live snapshot of the current analysis, if one exists -- keeps
        # the headline numbers visible in the sidebar without needing
        # to scroll back up to the Analysis tab.
        if mode == "single" and ats_score is not None:
            st.markdown(
                f"""
                <div class="sidebar-snapshot">
                    <div class="snapshot-heading">Current Analysis</div>
                    <div class="snapshot-row">
                        <div class="snapshot-stat">
                            <div class="snapshot-value">{ats_score}%</div>
                            <div class="snapshot-label">ATS Score</div>
                        </div>
                        <div class="snapshot-stat">
                            <div class="snapshot-value">{skill_match_percentage}%</div>
                            <div class="snapshot-label">Skill Match</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if api_key_missing:
            st.markdown(
                """
                <div class="alert-card">
                    No OpenRouter API key detected.<br><br>
                    AI-powered insights will be unavailable until
                    <code>OPENROUTER_API_KEY</code> is set in your
                    <code>.env</code> file. Rule-based ATS scoring and
                    skill matching still work.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            """
            <div class="sidebar-stack">
                <span>Python</span>
                <span>Streamlit</span>
                <span>OpenAI / OpenRouter</span>
                <span>scikit-learn</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return mode
