import streamlit as st


def render_upload_panel():
    with st.container(border=True):
        left, right = st.columns([1, 2], gap="large")

        with left:
            st.markdown("### 📄 Upload Resume")

            uploaded_resume = st.file_uploader(
                "",
                type=["pdf", "docx"],
                label_visibility="collapsed",
            )

        with right:
            st.markdown("### 📋 Job Description")

            job_description = st.text_area(
                "",
                placeholder="Paste the job description here...",
                height=230,
                label_visibility="collapsed",
            )

        st.write("")

        analyze = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
        )

    return uploaded_resume, job_description, analyze
