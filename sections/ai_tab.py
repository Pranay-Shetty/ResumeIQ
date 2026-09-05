import streamlit as st


def render_ai_tab(analysis, ai_error=None):

    st.header("AI Resume Analysis")

    if analysis is None:
        st.error(f"{ai_error or 'AI returned an invalid response.'}")
        return

    score_col, summary_col = st.columns([1, 2])

    with score_col:
        st.metric(
            "AI ATS Score",
            f"{analysis.ats_score}/100"
        )

    with summary_col:
        st.subheader("Professional Summary")
        st.write(analysis.professional_summary)

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Strengths")

        for strength in analysis.strengths:
            st.success(strength)

    with right:

        st.subheader("Weaknesses")

        for weakness in analysis.weaknesses:
            st.warning(weakness)

    st.divider()

    st.subheader("Missing Skills")

    if analysis.missing_skills:
        st.write(", ".join(analysis.missing_skills))
    else:
        st.success("No missing skills")

    st.divider()

    st.subheader("Suggestions")

    for suggestion in analysis.suggestions:
        st.info(suggestion)