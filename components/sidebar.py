import streamlit as st


def show_sidebar(api_key_missing: bool = False):

    with st.sidebar:

        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon">🤖</div>
                <div class="sidebar-brand-title">AI Resume Analyzer</div>
                <div class="sidebar-brand-version">Version 1.0</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-features">
                <div class="feature-item">✅ Resume Parsing</div>
                <div class="feature-item">✅ ATS Score</div>
                <div class="feature-item">✅ Skill Matching</div>
                <div class="feature-item">✅ AI Suggestions</div>
                <div class="feature-item">✅ PDF Report Export</div>
                <div class="feature-item soon">🔜 Cover Letter Generator</div>
                <div class="feature-item soon">🔜 Interview Questions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if api_key_missing:
            st.markdown(
                """
                <div class="alert-card">
                    ⚠ No OpenRouter API key detected.<br><br>
                    AI-powered insights will be unavailable until
                    <code>OPENROUTER_API_KEY</code> is set in your
                    <code>.env</code> file. Rule-based ATS scoring and
                    skill matching still work.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            """
            <div class="sidebar-stack">
                <span>🐍 Python</span>
                <span>⚡ Streamlit</span>
                <span>🤖 OpenAI / OpenRouter</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
