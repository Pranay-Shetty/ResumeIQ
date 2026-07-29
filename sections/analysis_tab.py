import streamlit as st

from components.dashboard_card import dashboard_card
from components.score_card import show_score
from components.skills_panel import show_skills
from components.charts import show_skill_chart


def render_analysis_tab(
    ats_score,
    skill_match_percentage,
    matched,
    missing,
):
    """
    Render Analysis Dashboard
    """

    # ==========================
    # Dashboard Header
    # ==========================

    st.markdown("## 📊 Dashboard")
    st.caption("Resume analysis results")

    st.write("")

    # ==========================
    # Dashboard Cards
    # ==========================

    dashboard_card(
        "ATS Score",
        f"{ats_score}%",
        "Resume Compatibility",
        "🎯",
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        dashboard_card(
            "Skill Match",
            f"{skill_match_percentage}%",
            "Job Match",
            "💼",
        )

    with col2:
        dashboard_card(
            "Matched Skills",
            str(len(matched)),
            "Skills Found",
            "✅",
        )

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
        dashboard_card(
            "Missing Skills",
            str(len(missing)),
            "Need Improvement",
            "❌",
        )

    with col4:
        dashboard_card(
            "AI Confidence",
            "High",
            "Analysis Complete",
            "🤖",
        )

    st.write("")
    st.divider()

    # ==========================
    # ATS Score
    # ==========================

    st.subheader("🎯 ATS Score")

    show_score(ats_score)

    st.divider()

    # ==========================
    # Skill Chart
    # ==========================

    st.subheader("📈 Skill Analysis")

    show_skill_chart(
        matched,
        missing,
    )

    st.divider()

    # ==========================
    # Skills Breakdown
    # ==========================

    st.subheader("🛠 Skills Breakdown")

    show_skills(
        matched,
        missing,
    )