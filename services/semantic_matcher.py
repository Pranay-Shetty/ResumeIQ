from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_content_similarity(resume_text: str, job_description: str) -> float:
    """
    Lightweight complement to the fixed skill-taxonomy match: a
    TF-IDF cosine similarity between the full resume and job
    description text. This is a lexical/statistical similarity (not
    a true embeddings-based semantic score -- that would need an
    embeddings API call or a downloaded transformer model), but it
    picks up relevant overlapping phrasing and context the fixed
    skill list misses, with no extra API cost or network dependency.

    Returns a 0-100 percentage.
    """
    if not resume_text or not job_description or not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english")

    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    except ValueError:
        # Happens if, after stopword removal, one of the documents
        # has no meaningful tokens left.
        return 0.0

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(float(similarity) * 100, 1)
