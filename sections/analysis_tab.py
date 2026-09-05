import streamlit as st

from components.dashboard_card import dashboard_card
from components.score_card import show_score
from components.score_breakdown import show_score_breakdown
from components.skills_panel import show_skills
from components.charts import show_skill_chart
from components.icons import (
    ICON_TARGET,
    ICON_CHECKLIST,
    ICON_CHECK_CIRCLE,
    ICON_ALERT,
    ICON_LAYERS,
    ICON_SPARKLE,
)


def render_analysis_tab(
    ats_score,
    skill_match_percentage,
    matched,
    missing,
    ats_breakdown=None,
    content_similarity=None,
):
    """
    Render Analysis Dashboard
    """

    # ==========================
    # Dashboard Header
    # ==========================

    st.markdown("## Dashboard")
    st.caption("Resume analysis results")

    st.write("")

    # ==========================
    # Dashboard Cards
    # ==========================

    dashboard_card(
        "ATS Score",
        f"{ats_score}%",
        "Resume Compatibility",
        icon=ICON_TARGET,
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        dashboard_card(
            "Skill Match",
            f"{skill_match_percentage}%",
            "Job Match",
            icon=ICON_CHECKLIST,
        )

    with col2:
        dashboard_card(
            "Matched Skills",
            str(len(matched)),
            "Skills Found",
            icon=ICON_CHECK_CIRCLE,
        )

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
        dashboard_card(
            "Missing Skills",
            str(len(missing)),
            "Need Improvement",
            icon=ICON_ALERT,
        )

    with col4:
        if content_similarity is not None:
            dashboard_card(
                "Content Similarity",
                f"{content_similarity}%",
                "TF-IDF Match to JD",
                icon=ICON_LAYERS,
            )
        else:
            dashboard_card(
                "AI Confidence",
                "High",
                "Analysis Complete",
                icon=ICON_SPARKLE,
            )

    st.write("")
    st.divider()

    # ==========================
    # ATS Score
    # ==========================

    st.subheader("ATS Score")

    show_score(ats_score)

    if ats_breakdown:
        st.write("")
        st.markdown("**Score Breakdown**")
        show_score_breakdown(ats_breakdown)

    st.divider()

    # ==========================
    # Skill Chart
    # ==========================

    st.subheader("Skill Analysis")

    show_skill_chart(
        matched,
        missing,
    )

    st.divider()

    # ==========================
    # Skills Breakdown
    # ==========================

    st.subheader("Skills Breakdown")

    show_skills(
        matched,
        missing,
    )
