import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from services.comparison_service import compare_resumes

MAX_RESUMES = 5
BAR_COLOR = "#2563EB"
TEXT_COLOR = "#E2E8F0"


def render_compare_section():

    st.markdown("## Compare Multiple Resumes")

    st.caption(
        f"Upload up to {MAX_RESUMES} resumes and score them all against "
        "the same job description -- useful for picking your strongest "
        "resume version, or for quickly screening several candidates."
    )

    st.write("")

    with st.container(border=True):
        uploaded_resumes = st.file_uploader(
            "Upload resumes",
            type=["pdf", "docx"],
            accept_multiple_files=True,
            key="compare_uploader",
        )

        job_description = st.text_area(
            "Job Description",
            placeholder="Paste the job description here...",
            height=200,
            key="compare_jd",
        )

        st.write("")

        compare_clicked = st.button(
            "Compare Resumes",
            type="primary",
            use_container_width=True,
        )

    if compare_clicked:
        if not uploaded_resumes:
            st.error("Upload at least one resume.")
        elif not job_description.strip():
            st.error("Please paste a job description.")
        elif len(uploaded_resumes) > MAX_RESUMES:
            st.error(f"Please upload {MAX_RESUMES} resumes or fewer at a time.")
        else:
            with st.spinner("Scoring resumes..."):
                st.session_state.compare_results = compare_resumes(
                    uploaded_resumes, job_description
                )

    results = st.session_state.get("compare_results")

    if not results:
        return

    st.divider()

    best = results[0]
    st.success(f"Strongest match: **{best['filename']}** (ATS score {best['ats_score']}%)")

    df = pd.DataFrame([
        {
            "Resume": r["filename"],
            "ATS Score": r["ats_score"],
            "Skill Match %": r["skill_match_percentage"],
            "Content Similarity %": r["content_similarity"],
            "Matched Skills": r["matched_count"],
            "Missing Skills": r["missing_count"],
        }
        for r in results
    ])

    st.dataframe(df, use_container_width=True, hide_index=True)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df["Resume"],
                y=df["ATS Score"],
                marker_color=BAR_COLOR,
                text=df["ATS Score"],
                textposition="outside",
            )
        ]
    )
    fig.update_layout(
        height=340,
        margin=dict(t=20, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(title="ATS Score", color=TEXT_COLOR, gridcolor="#334155"),
        xaxis=dict(color=TEXT_COLOR),
        font=dict(color=TEXT_COLOR),
    )
    st.plotly_chart(fig, use_container_width=True)

    if best["missing"]:
        preview = ", ".join(best["missing"][:8])
        if len(best["missing"]) > 8:
            preview += f", +{len(best['missing']) - 8} more"
        st.caption(f"Even the top match is missing: {preview}")
