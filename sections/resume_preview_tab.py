import streamlit as st


def render_resume_tab(resume_text):

    st.subheader("📄 Resume Preview")

    with st.expander(
        "View Extracted Resume",
        expanded=True
    ):
        st.text_area(
            label="",
            value=resume_text,
            height=500,
            disabled=True
        )