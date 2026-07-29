import streamlit as st


def render_upload_panel(reset_key=0):
    """
    reset_key changes whenever "Analyze Another Resume" is clicked
    (see app.py), which forces Streamlit to treat the file_uploader
    and text_area as brand-new widgets -- otherwise the previously
    uploaded file / pasted job description stick around after reset.
    """
    with st.container(border=True):
        left, right = st.columns([1, 2], gap="large")

        with left:
            st.markdown("### 📄 Upload Resume")

            uploaded_resume = st.file_uploader(
                "",
                type=["pdf", "docx"],
                label_visibility="collapsed",
                key=f"resume_uploader_{reset_key}",
            )

        with right:
            st.markdown("### 📋 Job Description")

            job_description = st.text_area(
                "",
                placeholder="Paste the job description here...",
                height=230,
                label_visibility="collapsed",
                key=f"job_description_{reset_key}",
            )

        st.write("")

        analyze = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary",
        )

    return uploaded_resume, job_description, analyze
