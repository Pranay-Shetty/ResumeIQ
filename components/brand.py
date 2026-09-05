"""
Shared brand assets for ResumeIQ: the actual logo artwork (a chrome/blue
lockup supplied by the project owner), inlined as base64 data URIs so a
single st.markdown() call can render logo + text together without
Streamlit needing to serve the file separately.

Two crops of the same source logo live in assets/:
  - resumeiq-logo-full.png  -- full lockup (icon + wordmark + tagline),
    used in the landing-page header.
  - resumeiq-logo-mark.png  -- the icon glyph only, cropped tight, used
    anywhere space is too narrow for the full lockup (the sidebar).
"""

import base64
from functools import lru_cache
from pathlib import Path

_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


@lru_cache(maxsize=None)
def _b64(filename: str) -> str:
    return base64.b64encode((_ASSETS_DIR / filename).read_bytes()).decode("ascii")


def brand_logo_full_html(width: int = 300) -> str:
    """Full ResumeIQ lockup (icon + wordmark + tagline) as an <img> tag."""
    return (
        '<img class="brand-logo-full" '
        f'src="data:image/png;base64,{_b64("resumeiq-logo-full.png")}" '
        f'alt="ResumeIQ -- Smarter Resumes. Brighter Opportunities." style="width:{width}px;">'
    )


def brand_mark_html(size: int = 32) -> str:
    """Small icon-only mark, for tight spaces like the sidebar."""
    return (
        '<img class="brand-mark-img" '
        f'src="data:image/png;base64,{_b64("resumeiq-logo-mark.png")}" '
        f'alt="ResumeIQ" style="width:{size}px;height:{size}px;">'
    )
