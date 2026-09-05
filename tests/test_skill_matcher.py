from services.skill_matcher import compare_skills


def test_matched_and_missing_are_split_correctly():
    resume_skills = ["Python", "SQL", "AWS"]
    jd_skills = ["Python", "Docker"]

    matched, missing = compare_skills(resume_skills, jd_skills)

    assert matched == ["Python"]
    assert missing == ["Docker"]


def test_no_overlap():
    matched, missing = compare_skills(["Java"], ["Python"])
    assert matched == []
    assert missing == ["Python"]


def test_empty_jd_skills_means_nothing_missing():
    matched, missing = compare_skills(["Python"], [])
    assert matched == []
    assert missing == []


def test_results_are_sorted():
    matched, missing = compare_skills(
        ["Python", "AWS", "SQL"],
        ["SQL", "AWS", "Python", "Docker"],
    )
    assert matched == sorted(matched)
    assert missing == sorted(missing)
