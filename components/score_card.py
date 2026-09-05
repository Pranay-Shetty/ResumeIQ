import streamlit as st


def show_score(score: int):

    st.subheader("ATS Analysis")

    progress = score / 100

    col1, col2 = st.columns([3, 1])

    with col1:
        st.progress(progress)

    with col2:
        st.metric("ATS Score", f"{score}%")

    if score >= 90:
        st.success("Outstanding Resume")
    elif score >= 80:
        st.success("Excellent ATS Compatibility")
    elif score >= 70:
        st.info("Good Resume")
    elif score >= 60:
        st.warning("Can Be Improved")
    else:
        st.error("Needs Significant Improvement")