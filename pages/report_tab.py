import streamlit as st

from services.report_generator import generate_report_pdf


def render_report_tab(
    ats_score,
    skill_match_percentage,
    matched,
    missing,
    analysis,
):
    """
    Render the downloadable PDF report tab.
    """

    st.subheader("📥 Download Your Report")

    st.caption(
        "Export a PDF summary of your ATS score, skill match, "
        "and AI-powered insights to share or keep for reference."
    )

    st.write("")

    try:
        pdf_bytes = generate_report_pdf(
            ats_score=ats_score,
            skill_match_percentage=skill_match_percentage,
            matched_skills=matched,
            missing_skills=missing,
            analysis=analysis,
        )

        st.download_button(
            label="⬇️ Download Analysis Report (PDF)",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

        st.success("Report ready. Click above to download.")

    except Exception as e:
        st.error(f"Could not generate the report: {e}")
