import streamlit as st


def show_footer():

    st.divider()

    st.markdown(
        '<div class="app-footer">Built with ❤️ using Python, Streamlit and OpenAI</div>',
        unsafe_allow_html=True,
    )
