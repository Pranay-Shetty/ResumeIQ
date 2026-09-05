"""
Shared brand mark (logo) for ResumeIQ.

A single small, flat SVG icon -- a document with a folded corner and a
checkmark badge, standing in for "your resume, scored" -- used in both
the landing-page header and the sidebar brand block. Keeping it in one
place means a future icon tweak is a single edit, not a hunt across
components.
"""

BRAND_MARK_SVG = (
    '<svg class="brand-mark" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" '
    'role="img" aria-label="ResumeIQ logo">'
    '<path class="brand-mark-page" d="M10 4h14l6 6v26a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/>'
    '<path class="brand-mark-fold" d="M24 4v6h6z"/>'
    '<line class="brand-mark-line" x1="13" y1="17" x2="27" y2="17"/>'
    '<line class="brand-mark-line" x1="13" y1="22" x2="27" y2="22"/>'
    '<line class="brand-mark-line" x1="13" y1="27" x2="20" y2="27"/>'
    '<circle class="brand-mark-badge" cx="30" cy="31" r="6.5"/>'
    '<path class="brand-mark-check" d="M26.8 31.2l2.4 2.3 4.4-4.8"/>'
    '</svg>'
)
