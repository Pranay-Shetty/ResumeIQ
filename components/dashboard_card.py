import streamlit as st


def dashboard_card(title, value, subtitle="", icon=""):
    """
    Renders a single stat card (icon, title, big value, subtitle)
    using the .dashboard-card component classes from styles.css.
    """

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="dashboard-icon">{icon}</div>
            <div class="dashboard-title">{title}</div>
            <div class="dashboard-value">{value}</div>
            <div class="dashboard-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
