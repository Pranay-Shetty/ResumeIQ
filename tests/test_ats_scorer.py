from services.ats_scorer import calculate_ats_score, calculate_ats_score_breakdown

GOOD_LENGTH_RESUME = " ".join(["experience"] * 500)


def test_full_skill_match_scores_max_skill_points():
    breakdown = calculate_ats_score_breakdown(
        resume_text="irrelevant",
        matched_skills=["Python", "SQL"],
        jd_skills=["Python", "SQL"],
    )
    assert breakdown["skill_match"]["score"] == 60


def test_no_jd_skills_gives_full_skill_credit():
    breakdown = calculate_ats_score_breakdown(
        resume_text="irrelevant",
        matched_skills=[],
        jd_skills=[],
    )
    assert breakdown["skill_match"]["score"] == 60


def test_partial_skill_match_is_proportional():
    breakdown = calculate_ats_score_breakdown(
        resume_text="irrelevant",
        matched_skills=["Python"],
        jd_skills=["Python", "SQL"],
    )
    assert breakdown["skill_match"]["score"] == 30


def test_ideal_length_scores_max_length_points():
    breakdown = calculate_ats_score_breakdown(
        resume_text=GOOD_LENGTH_RESUME,
        matched_skills=[],
        jd_skills=[],
    )
    assert breakdown["length"]["score"] == 15


def test_very_short_resume_scores_low_length_points():
    breakdown = calculate_ats_score_breakdown(
        resume_text="too short",
        matched_skills=[],
        jd_skills=[],
    )
    assert breakdown["length"]["score"] == 4


def test_contact_info_detects_email_and_phone():
    resume_text = "Contact: jane.doe@example.com, +1 555-123-4567"
    breakdown = calculate_ats_score_breakdown(resume_text, [], [])
    assert breakdown["contact"]["score"] == 10


def test_contact_info_missing_scores_zero():
    breakdown = calculate_ats_score_breakdown("No contact details here.", [], [])
    assert breakdown["contact"]["score"] == 0


def test_quantified_achievements_detects_numbers_in_long_lines():
    resume_text = (
        "Led a cross-functional team of 8 engineers to ship the new billing platform\n"
        "Owned end-to-end delivery of a vague and unquantified initiative overall\n"
    )
    breakdown = calculate_ats_score_breakdown(resume_text, [], [])
    assert 0 < breakdown["achievements"]["score"] < 15


def test_total_score_matches_sum_of_breakdown():
    matched, jd_skills = ["Python"], ["Python", "SQL"]
    resume_text = GOOD_LENGTH_RESUME + " jane.doe@example.com 555-123-4567"

    total = calculate_ats_score(resume_text, matched, jd_skills)
    breakdown = calculate_ats_score_breakdown(resume_text, matched, jd_skills)

    assert total == round(sum(c["score"] for c in breakdown.values()))


def test_breakdown_categories_sum_to_100_max():
    breakdown = calculate_ats_score_breakdown("x", [], [])
    assert sum(c["max"] for c in breakdown.values()) == 100
