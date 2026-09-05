import streamlit as st

from services.history_service import clear_history, get_history, restore_from_history


def render_history_section():

    st.markdown("## Analysis History")

    st.caption(
        "Past analyses from this session -- reload any of them to revisit "
        "the full results without re-uploading the resume or re-running "
        "the AI calls. This history lives only in your current browser "
        "session; it isn't saved to disk and resets if the app restarts."
    )

    history = get_history()

    if not history:
        st.info(
            "No analyses yet. Run one from \"Analyze One Resume\" and "
            "it'll show up here."
        )
        return

    st.write("")

    if st.button("Clear History"):
        clear_history()
        st.rerun()

    st.write("")

    for entry in history:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([3, 1.2, 1.2, 1.2, 1.3])

            with col1:
                st.markdown(f"**{entry.get('uploaded_resume_name') or 'Resume'}**")
                st.caption(entry["analyzed_at"])

            with col2:
                st.metric("ATS", f"{entry.get('ats_score', 0)}%")

            with col3:
                st.metric("Skill Match", f"{entry.get('skill_match_percentage', 0)}%")

            with col4:
                similarity = entry.get("content_similarity")
                st.metric("Similarity", f"{similarity}%" if similarity is not None else "—")

            with col5:
                st.write("")
                st.write("")
                if st.button("Reload", key=f"reload_{entry['id']}", use_container_width=True):
                    restore_from_history(entry["id"])
                    st.rerun()
