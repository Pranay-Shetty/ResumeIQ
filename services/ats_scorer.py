import re


def _count_quantified_lines(resume_text):
    """
    Rough heuristic for "quantified achievements": how many
    substantial lines (long enough to plausibly be a bullet point,
    not a header/name/date) contain a number, percentage, or
    currency amount.
    """
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    content_lines = [line for line in lines if len(line) >= 25]

    if not content_lines:
        return 0, 0

    quantified = [line for line in content_lines if re.search(r"\d", line)]

    return len(quantified), len(content_lines)


def calculate_ats_score_breakdown(resume_text, matched_skills, jd_skills):
    """
    Breaks the rule-based ATS score down into the categories that
    make it up, so the UI can show *why* a resume scored what it
    scored instead of just a single opaque number.

    Categories and weights (sum to 100):
      - Keyword / Skill Match     : 60
      - Quantified Achievements   : 15
      - Resume Length             : 15
      - Contact Info              : 10
    """
    breakdown = {}

    # ---------- Keyword / Skill Match (60 points) ----------
    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 60
        skill_detail = f"{len(matched_skills)} of {len(jd_skills)} required skills found"
    else:
        skill_score = 60
        skill_detail = "No specific skills required by this job description"

    breakdown["skill_match"] = {
        "label": "Keyword / Skill Match",
        "score": round(skill_score, 1),
        "max": 60,
        "detail": skill_detail,
    }

    # ---------- Quantified Achievements (15 points) ----------
    quantified, total_lines = _count_quantified_lines(resume_text)

    if total_lines:
        achievement_score = round((quantified / total_lines) * 15, 1)
        achievement_detail = f"{quantified} of {total_lines} lines include a number or metric"
    else:
        achievement_score = 0
        achievement_detail = "Not enough resume text to evaluate"

    breakdown["achievements"] = {
        "label": "Quantified Achievements",
        "score": achievement_score,
        "max": 15,
        "detail": achievement_detail,
    }

    # ---------- Resume Length (15 points) ----------
    words = len(resume_text.split())

    if 300 <= words <= 1000:
        length_score = 15
    elif 200 <= words < 300:
        length_score = 11
    elif words > 1000:
        length_score = 11
    else:
        length_score = 4

    breakdown["length"] = {
        "label": "Resume Length",
        "score": length_score,
        "max": 15,
        "detail": f"{words} words",
    }

    # ---------- Contact Info (10 points) ----------
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text)

    # Matches common phone formats: (555) 123-4567, 555-123-4567,
    # 555.123.4567, +91 98765 43210, 9876543210, etc.
    phone = re.search(
        r"(\+\d{1,3}[\s.-]?)?"
        r"(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b",
        resume_text,
    )

    contact_score = (5 if email else 0) + (5 if phone else 0)
    found = []
    if email:
        found.append("email")
    if phone:
        found.append("phone")

    breakdown["contact"] = {
        "label": "Contact Info",
        "score": contact_score,
        "max": 10,
        "detail": (", ".join(found).capitalize() + " found") if found else "No email or phone detected",
    }

    return breakdown


def calculate_ats_score(resume_text, matched_skills, jd_skills):
    """
    Total rule-based ATS score (0-100). Kept as a thin wrapper around
    calculate_ats_score_breakdown so existing callers that only need
    the single number don't have to change.
    """
    breakdown = calculate_ats_score_breakdown(resume_text, matched_skills, jd_skills)
    return round(sum(category["score"] for category in breakdown.values()))
