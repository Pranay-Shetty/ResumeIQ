from services.semantic_matcher import calculate_content_similarity


def test_identical_text_scores_high_similarity():
    text = "Experienced Python developer with AWS and Docker background."
    similarity = calculate_content_similarity(text, text)
    assert similarity > 90


def test_unrelated_text_scores_low_similarity():
    resume = "Experienced pastry chef specializing in French desserts."
    jd = "Senior backend engineer with Kubernetes and Go experience."
    similarity = calculate_content_similarity(resume, jd)
    assert similarity < 40


def test_empty_inputs_return_zero():
    assert calculate_content_similarity("", "something") == 0.0
    assert calculate_content_similarity("something", "") == 0.0
    assert calculate_content_similarity("", "") == 0.0
    assert calculate_content_similarity(None, "something") == 0.0


def test_returns_a_percentage_range():
    similarity = calculate_content_similarity(
        "Python developer with SQL experience",
        "Looking for a Python engineer familiar with databases",
    )
    assert 0.0 <= similarity <= 100.0
