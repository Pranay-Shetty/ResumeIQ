import streamlit as st

from services.cover_letter_service import generate_cover_letter

TONES = ["Professional", "Enthusiastic", "Concise"]


def render_cover_letter_tab(resume_text, job_description):

    st.header("Cover Letter Generator")

    st.caption(
        "Generate a tailored cover letter on demand -- pick a tone, "
        "generate, then edit freely before downloading."
    )

    st.write("")

    tone = st.selectbox("Tone", TONES, key="cover_letter_tone")

    if st.button("Generate Cover Letter", type="primary"):
        with st.spinner("Writing your cover letter..."):
            letter, error = generate_cover_letter(resume_text, job_description, tone)
            st.session_state.cover_letter = letter
            st.session_state.cover_letter_error = error

    error = st.session_state.get("cover_letter_error")
    letter = st.session_state.get("cover_letter")

    if error:
        st.error(f"{error}")

    if letter is not None:
        st.write("")

        edited_letter = st.text_area(
            "Edit before downloading",
            value=letter.cover_letter,
            height=400,
        )

        st.download_button(
            "Download Cover Letter (.txt)",
            data=edited_letter,
            file_name="cover_letter.txt",
            mime="text/plain",
            use_container_width=True,
        )
