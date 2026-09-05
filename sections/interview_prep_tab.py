import streamlit as st


def render_interview_prep_tab(interview_prep, error=None):

    st.header("Interview Preparation")

    if interview_prep is None:
        st.error(error or "Interview prep could not be generated.")
        return

    st.caption(
        "AI-generated questions tailored to this job description, with "
        "suggested answers drawn from your resume -- use these to practice, "
        "not to memorize word-for-word."
    )

    st.write("")

    for i, q in enumerate(interview_prep.questions, start=1):
        with st.expander(f"{i}. {q.question}"):
            st.caption(q.category)
            st.markdown("**Suggested Answer**")
            st.write(q.suggested_answer)

    if interview_prep.tips:
        st.divider()
        st.subheader("Tips For This Role")

        for tip in interview_prep.tips:
            st.info(tip)
