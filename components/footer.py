def show_footer():
    """
    Intentionally minimal. Earlier versions rendered a "Built with..."
    tech-stack line here -- dropped for a cleaner, more professional
    footprint on the page (an end user doesn't need to know the stack
    a tool is built on). Kept as a no-op function, rather than removing
    the call sites, so a real footer (e.g. a version tag or a link)
    can be added later without touching app.py.
    """
    return
