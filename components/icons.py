"""
Small icon badges used on feature cards and dashboard stat cards.

Each badge is a circular gradient chip (styled in assets/styles.css via
the .icon-badge class) with a simple white line-icon inside. Kept as
plain, single-line SVG strings -- no embedded newlines -- so they stay
safe to splice into the single-call st.markdown() HTML blocks used by
components/feature_grid.py and components/dashboard_card.py (a
multi-line raw-HTML block that hits a blank line gets mis-parsed by
Streamlit's markdown renderer; see feature_grid.py for the story).
"""

_ICON_ATTRS = (
    'viewBox="0 0 24 24" width="20" height="20" fill="none" '
    'stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
)


def _badge(inner_svg: str) -> str:
    return (
        f'<span class="icon-badge"><svg {_ICON_ATTRS}>{inner_svg}</svg></span>'
    )


# ATS Score / target
ICON_TARGET = _badge(
    '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4.2"/>'
    '<circle cx="12" cy="12" r="0.6" fill="white"/>'
)

# Skill Match / checklist
ICON_CHECKLIST = _badge(
    '<rect x="4" y="3.5" width="16" height="17" rx="2.2"/>'
    '<polyline points="7.5 11 10 13.5 16.5 7"/>'
    '<line x1="7.5" y1="16.5" x2="16.5" y2="16.5"/>'
)

# Matched Skills / check-circle
ICON_CHECK_CIRCLE = _badge(
    '<circle cx="12" cy="12" r="8.5"/><polyline points="8 12.5 10.8 15.2 16 9.3"/>'
)

# Missing Skills / alert
ICON_ALERT = _badge(
    '<path d="M12 3.5 21 19H3z"/><line x1="12" y1="9.5" x2="12" y2="13.5"/>'
    '<circle cx="12" cy="16.3" r="0.6" fill="white"/>'
)

# Content Similarity / layers
ICON_LAYERS = _badge(
    '<polygon points="12 3.5 20.5 8 12 12.5 3.5 8"/>'
    '<polyline points="3.5 12 12 16.5 20.5 12"/>'
    '<polyline points="3.5 16 12 20.5 20.5 16"/>'
)

# AI Confidence / AI Analysis / sparkle
ICON_SPARKLE = _badge(
    '<path d="M12 3.5 13.6 9 19 10.6 13.6 12.2 12 17.7 10.4 12.2 5 10.6 10.4 9z"/>'
    '<path d="M19 3.5 19.6 5.4 21.5 6 19.6 6.6 19 8.5 18.4 6.6 16.5 6 18.4 5.4z"/>'
)

# Rewrite Suggestions / pencil
ICON_EDIT = _badge(
    '<path d="M4 20l1-4.6L15.6 4.8a1.8 1.8 0 0 1 2.6 0l1 1a1.8 1.8 0 0 1 0 2.6L8.6 19 4 20z"/>'
    '<line x1="14" y1="6.4" x2="17.6" y2="10"/>'
)

# Interview Prep / message
ICON_MESSAGE = _badge(
    '<path d="M4 5.5h16v11H10l-4 3.5v-3.5H4z"/>'
    '<line x1="7.5" y1="9.5" x2="16.5" y2="9.5"/>'
    '<line x1="7.5" y1="13" x2="13.5" y2="13"/>'
)

# Cover Letter Generator / mail
ICON_MAIL = _badge(
    '<rect x="3.5" y="5.5" width="17" height="13" rx="1.8"/>'
    '<polyline points="3.5 6.5 12 13 20.5 6.5"/>'
)

# Compare Resumes / bar chart
ICON_COMPARE = _badge(
    '<line x1="5" y1="20" x2="5" y2="11"/>'
    '<line x1="12" y1="20" x2="12" y2="5"/>'
    '<line x1="19" y1="20" x2="19" y2="14"/>'
)
