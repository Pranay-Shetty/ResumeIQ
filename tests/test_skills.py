from utils.skills import extract_skills


def test_extracts_known_skills_case_insensitively():
    text = "Experienced PYTHON developer with SQL and AWS background."
    skills = extract_skills(text)

    assert "Python" in skills
    assert "SQL" in skills
    assert "AWS" in skills


def test_ignores_unrelated_words():
    skills = extract_skills("Went for a walk and had a great cup of coffee.")
    assert skills == []


def test_specific_variant_supersedes_generic_one():
    # Both "react" and "react.js" match the same mention -- only the
    # more specific one should be kept (see _SUPERSEDED_BY).
    skills = extract_skills("Built the frontend using React.js.")
    assert "React.js" in skills
    assert "React" not in skills


def test_special_characters_in_skill_names_are_matched():
    skills = extract_skills("Backend written in C++ with a bit of C#.")
    assert "C++" in skills
    assert "C#" in skills


def test_empty_text_returns_empty_list():
    assert extract_skills("") == []
    assert extract_skills(None) == []
