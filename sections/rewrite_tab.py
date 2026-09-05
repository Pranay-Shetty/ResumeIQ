import streamlit as st


def render_rewrite_tab(rewrite, error=None):

    st.header("✍️ Resume Rewrite Suggestions")

    if rewrite is None:
        st.error(f"❌ {error or 'Rewrite suggestions could not be generated.'}")
        return

    st.caption(
        "AI-identified weak lines from your resume, rewritten to be "
        "stronger and tailored to this job description -- use these as "
        "a starting point, not a copy-paste replacement."
    )

    st.write("")

    if not rewrite.rewrites:
        st.success("No weak lines detected -- your resume already reads strong 🎉")
    else:
        for i, item in enumerate(rewrite.rewrites, start=1):
            with st.container(border=True):
                st.markdown(f"**{i}. Original**")
                st.markdown(f"> {item.original}")
                st.markdown("**Improved**")
                st.success(item.improved)
                st.caption(f"💡 {item.reason}")

    if rewrite.general_advice:
        st.divider()
        st.subheader("📎 General Advice")

        for advice in rewrite.general_advice:
            st.info(advice)
