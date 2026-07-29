import re


def calculate_ats_score(resume_text, matched_skills, jd_skills):
    """
    Calculate a simple ATS score.
    """

    score = 0

    # ---------- Skill Match (70 points) ----------
    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 70
    else:
        skill_score = 70

    score += skill_score

    # ---------- Resume Length (20 points) ----------
    words = len(resume_text.split())

    if 300 <= words <= 1000:
        score += 20
    elif 200 <= words < 300:
        score += 15
    elif words > 1000:
        score += 15
    else:
        score += 5

    # ---------- Contact Info (10 points) ----------
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume_text)

    # Matches common phone formats: (555) 123-4567, 555-123-4567,
    # 555.123.4567, +91 98765 43210, 9876543210, etc.
    phone = re.search(
        r"(\+\d{1,3}[\s.-]?)?"
        r"(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}\b",
        resume_text,
    )

    if email:
        score += 5

    if phone:
        score += 5

    return round(score)