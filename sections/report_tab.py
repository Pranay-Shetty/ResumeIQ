import streamlit as st

from services.report_generator import generate_report_pdf


def render_report_tab(
    ats_score,
    skill_match_percentage,
    matched,
    missing,
    analysis,
    interview_prep=None,
    ats_breakdown=None,
    content_similarity=None,
    rewrite=None,
):
    """
    Render the downloadable PDF report tab.
    """

    st.subheader("Download Your Report")

    st.caption(
        "Export a PDF summary of your ATS score breakdown, skill match, "
        "AI-powered insights, rewrite suggestions, and interview prep "
        "questions to share or keep for reference. If you generated a "
        "cover letter, it's included too."
    )

    st.write("")

    try:
        pdf_bytes = generate_report_pdf(
            ats_score=ats_score,
            skill_match_percentage=skill_match_percentage,
            matched_skills=matched,
            missing_skills=missing,
            analysis=analysis,
            interview_prep=interview_prep,
            ats_breakdown=ats_breakdown,
            content_similarity=content_similarity,
            rewrite=rewrite,
            cover_letter=st.session_state.get("cover_letter"),
        )

        st.download_button(
            label="Download Analysis Report (PDF)",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        st.success("Report ready. Click above to download.")

    except Exception as e:
        st.error(f"Could not generate the report: {e}")
