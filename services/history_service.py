import uuid
from datetime import datetime

import streamlit as st

# Kept in sync with app.RESULT_KEYS -- everything a full "reload" of a
# past analysis needs to restore into the live session state.
SNAPSHOT_KEYS = (
    "resume_text",
    "job_description",
    "matched",
    "missing",
    "ats_score",
    "ats_breakdown",
    "content_similarity",
    "skill_match_percentage",
    "analysis",
    "ai_error",
    "interview_prep",
    "interview_prep_error",
    "rewrite",
    "rewrite_error",
    "uploaded_resume_name",
)


def add_to_history():
    """
    Snapshots the just-completed analysis into session-scoped history
    so the user can revisit past runs without re-uploading the resume
    or re-running the AI calls.

    This is in-memory only, scoped to the current Streamlit session --
    it is NOT written to disk or a database, and resets if the app
    server restarts or the browser session ends. Making it durable
    across restarts would need a real datastore, which is a bigger
    change than this app's current scope.
    """
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []

    entry = {key: st.session_state.get(key) for key in SNAPSHOT_KEYS}
    entry["id"] = str(uuid.uuid4())
    entry["analyzed_at"] = datetime.now().strftime("%b %d, %Y %I:%M %p")

    st.session_state.analysis_history.insert(0, entry)


def get_history():
    return st.session_state.get("analysis_history", [])


def clear_history():
    st.session_state.analysis_history = []


def restore_from_history(entry_id) -> bool:
    """
    Copies a past analysis snapshot back into the live single-resume
    session state and switches the app into single-analysis mode, so
    the full set of result tabs shows that run again. Returns False
    if the entry no longer exists (e.g. history was cleared).
    """
    entry = next((e for e in get_history() if e["id"] == entry_id), None)

    if entry is None:
        return False

    for key in SNAPSHOT_KEYS:
        st.session_state[key] = entry[key]

    st.session_state.analysis_complete = True
    st.session_state.show_summary_dialog = False
    st.session_state.app_mode = "🔍 Analyze One Resume"

    return True
