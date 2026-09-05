import streamlit as st


def dashboard_card(title, value, subtitle=""):
    """
    Renders a single stat card (title, big value, subtitle) using the
    .dashboard-card component classes from styles.css.
    """

    st.markdown(
        f'<div class="dashboard-card">'
        f'<div class="dashboard-title">{title}</div>'
        f'<div class="dashboard-value">{value}</div>'
        f'<div class="dashboard-subtitle">{subtitle}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
