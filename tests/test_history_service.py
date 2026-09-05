"""
history_service reads/writes st.session_state directly, so these
tests fake just enough of Streamlit's session_state (a dict with
attribute access) rather than requiring a real Streamlit runtime.
"""

import importlib
import sys
import types


class _FakeSessionState(dict):
    """Minimal stand-in for st.session_state: dict + attribute access."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e

    def __setattr__(self, name, value):
        self[name] = value


def _install_fake_streamlit(monkeypatch):
    fake_st = types.ModuleType("streamlit")
    fake_st.session_state = _FakeSessionState()
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)
    return fake_st


def test_add_to_history_snapshots_current_state(monkeypatch):
    fake_st = _install_fake_streamlit(monkeypatch)
    from services import history_service
    importlib.reload(history_service)

    fake_st.session_state.ats_score = 82
    fake_st.session_state.skill_match_percentage = 70
    fake_st.session_state.uploaded_resume_name = "resume.pdf"

    history_service.add_to_history()
    history = history_service.get_history()

    assert len(history) == 1
    assert history[0]["ats_score"] == 82
    assert history[0]["uploaded_resume_name"] == "resume.pdf"
    assert "id" in history[0]
    assert "analyzed_at" in history[0]


def test_history_newest_first(monkeypatch):
    fake_st = _install_fake_streamlit(monkeypatch)
    from services import history_service
    importlib.reload(history_service)

    fake_st.session_state.uploaded_resume_name = "first.pdf"
    history_service.add_to_history()

    fake_st.session_state.uploaded_resume_name = "second.pdf"
    history_service.add_to_history()

    history = history_service.get_history()
    assert history[0]["uploaded_resume_name"] == "second.pdf"
    assert history[1]["uploaded_resume_name"] == "first.pdf"


def test_clear_history_empties_list(monkeypatch):
    fake_st = _install_fake_streamlit(monkeypatch)
    from services import history_service
    importlib.reload(history_service)

    history_service.add_to_history()
    assert len(history_service.get_history()) == 1

    history_service.clear_history()
    assert history_service.get_history() == []


def test_restore_from_history_repopulates_session_state(monkeypatch):
    fake_st = _install_fake_streamlit(monkeypatch)
    from services import history_service
    importlib.reload(history_service)

    fake_st.session_state.ats_score = 55
    fake_st.session_state.uploaded_resume_name = "old.pdf"
    history_service.add_to_history()

    entry_id = history_service.get_history()[0]["id"]

    fake_st.session_state.ats_score = 0
    fake_st.session_state.uploaded_resume_name = None

    restored = history_service.restore_from_history(entry_id)

    assert restored is True
    assert fake_st.session_state.ats_score == 55
    assert fake_st.session_state.uploaded_resume_name == "old.pdf"
    assert fake_st.session_state.analysis_complete is True
    assert fake_st.session_state.app_mode == "🔍 Analyze One Resume"


def test_restore_from_history_returns_false_for_unknown_id(monkeypatch):
    _install_fake_streamlit(monkeypatch)
    from services import history_service
    importlib.reload(history_service)

    assert history_service.restore_from_history("does-not-exist") is False
