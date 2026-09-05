import streamlit as st


def dashboard_card(title, value, subtitle="", icon=""):
    """
    Renders a single stat card (title, big value, subtitle, optional
    icon badge) using the .dashboard-card component classes from
    styles.css. `icon` is a pre-built icon-badge HTML string from
    components/icons.py -- pass "" to omit it.
    """

    st.markdown(
        f'<div class="dashboard-card">'
        f'{icon}'
        f'<div class="dashboard-title">{title}</div>'
        f'<div class="dashboard-value">{value}</div>'
        f'<div class="dashboard-subtitle">{subtitle}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
