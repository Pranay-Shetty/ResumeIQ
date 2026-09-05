import streamlit as st


def show_score_breakdown(breakdown: dict):
    """
    Renders a per-category progress bar for the ATS score breakdown
    returned by services.ats_scorer.calculate_ats_score_breakdown, so
    a resume's score is explained rather than just a single number.
    """
    for category in breakdown.values():
        score = category["score"]
        max_score = category["max"] or 1
        fraction = min(max(score / max_score, 0), 1)

        col1, col2 = st.columns([4, 1])

        with col1:
            st.caption(f"**{category['label']}** · {category.get('detail', '')}")
            st.progress(fraction)

        with col2:
            st.markdown(f"<div style='text-align:right; padding-top:8px;'>{score:.0f}/{category['max']}</div>", unsafe_allow_html=True)
