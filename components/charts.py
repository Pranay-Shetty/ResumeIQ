import plotly.graph_objects as go
import streamlit as st

MATCHED_COLOR = "#2563EB"
MISSING_COLOR = "#334155"
TEXT_COLOR = "#E2E8F0"
MUTED_COLOR = "#94A3B8"


def show_skill_chart(matched, missing):
    """
    Donut chart showing skill-match coverage, with the match
    percentage displayed in the center -- easier to read at a
    glance than a bar per individual skill.
    """

    total = len(matched) + len(missing)

    if total == 0:
        st.info("No skills detected yet -- upload a resume and job description to see coverage.")
        return

    match_pct = round((len(matched) / total) * 100)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Matched", "Missing"],
                values=[len(matched), len(missing)],
                hole=0.68,
                marker=dict(
                    colors=[MATCHED_COLOR, MISSING_COLOR],
                    line=dict(color="#0F172A", width=3),
                ),
                textinfo="label+value",
                textfont=dict(size=13, color=TEXT_COLOR),
                sort=False,
                direction="clockwise",
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        height=340,
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[
            dict(
                text=(
                    f"<span style='font-size:32px;font-weight:800;color:{TEXT_COLOR}'>{match_pct}%</span>"
                    f"<br><span style='font-size:12px;color:{MUTED_COLOR}'>Skill Match</span>"
                ),
                x=0.5,
                y=0.5,
                showarrow=False,
            )
        ],
    )

    st.plotly_chart(fig, use_container_width=True)
