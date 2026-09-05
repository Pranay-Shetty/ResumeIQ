import streamlit as st


def create_chip(skill: str, kind: str) -> str:
    """
    kind is either "matched" or "missing" -- maps to the
    .skill-chip--matched / .skill-chip--missing classes.
    """
    return f'<span class="skill-chip skill-chip--{kind}">{skill}</span>'


def show_skills(matched, missing):

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matched Skills")

        if matched:
            html = "".join(create_chip(skill, "matched") for skill in sorted(matched))
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No matched skills found.")

    with col2:

        st.subheader("Missing Skills")

        if missing:
            html = "".join(create_chip(skill, "missing") for skill in sorted(missing))
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.success("No missing skills")
