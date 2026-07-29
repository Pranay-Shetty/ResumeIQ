import streamlit as st


def show_sidebar(api_key_missing: bool = False):

    with st.sidebar:

        st.header("📋 Menu")

        st.info(
            """
            ### AI Resume Analyzer

            Version **1.0**

            #### Features

            ✅ Resume Parsing

            ✅ ATS Score

            ✅ Skill Matching

            ✅ AI Suggestions

            ✅ PDF Report Export

            🔜 Cover Letter Generator

            🔜 Interview Questions
            """
        )

        if api_key_missing:
            st.warning(
                "⚠ No OpenRouter API key detected.\n\n"
                "AI-powered insights will be unavailable until "
                "`OPENROUTER_API_KEY` is set in your `.env` file. "
                "Rule-based ATS scoring and skill matching still work."
            )

        st.markdown("---")

        st.write("Developed using")

        st.write("🐍 Python")

        st.write("⚡ Streamlit")

        st.write("🤖 OpenAI / OpenRouter")