import streamlit as st

FEATURES = [
    ("ATS Score Breakdown", "See exactly why your resume scored what it did, broken down by keyword match, achievements, length, and contact info."),
    ("AI Resume Analysis", "Get recruiter-style strengths, weaknesses, and a tailored professional summary."),
    ("Rewrite Suggestions", "Weak resume lines rewritten to be stronger and tailored to the job description, with the reasoning behind each change."),
    ("Interview Prep", "Practice with role-specific interview questions and suggested answers drawn from your own resume."),
    ("Cover Letter Generator", "Generate a tailored, editable cover letter in the tone you choose, ready to download."),
    ("Compare Resumes", "Score multiple resume versions against the same job description, side by side, ranked by fit."),
]


def show_feature_highlights():
    """
    A compact, always-visible showcase of what the tool can do, shown
    on the landing/upload screen so a first-time user sees the full
    feature set up front.

    Renders each card as its own st.markdown call inside a Streamlit
    column, rather than one big HTML string for the whole grid. The
    earlier single-string approach broke: a blank line between
    concatenated <div> blocks closed Streamlit's raw-HTML block early
    (CommonMark's rule for HTML blocks), and the indented text for
    later cards then got parsed as a literal Markdown code block
    instead of HTML -- which is exactly the "raw code visible on the
    page" bug this replaced. One call per card, each a single line
    with no internal blank lines, sidesteps that entirely.
    """
    rows = [FEATURES[i:i + 3] for i in range(0, len(FEATURES), 3)]

    for row in rows:
        columns = st.columns(len(row))
        for column, (title, desc) in zip(columns, row):
            with column:
                st.markdown(
                    f'<div class="feature-card">'
                    f'<div class="feature-card-title">{title}</div>'
                    f'<div class="feature-card-desc">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
