import io

from docx import Document as DocxDocument

from services.comparison_service import compare_resumes


def _make_docx_file(name, paragraphs):
    doc = DocxDocument()
    for paragraph in paragraphs:
        doc.add_paragraph(paragraph)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    buffer.name = name
    return buffer


def test_compare_resumes_ranks_stronger_resume_first():
    strong_resume = _make_docx_file(
        "strong.docx",
        [
            "Jane Doe",
            "jane@example.com",
            "555-123-4567",
            "Senior Python developer with AWS, Docker, and SQL experience.",
        ],
    )
    weak_resume = _make_docx_file(
        "weak.docx",
        ["John Roe", "Marketing coordinator with no technical background."],
    )

    job_description = "Looking for a Python developer with AWS, Docker, and SQL skills."

    results = compare_resumes([strong_resume, weak_resume], job_description)

    assert len(results) == 2
    assert results[0]["filename"] == "strong.docx"
    assert results[0]["ats_score"] >= results[1]["ats_score"]
    assert results == sorted(results, key=lambda r: r["ats_score"], reverse=True)


def test_compare_resumes_skips_unsupported_extensions():
    bogus = io.BytesIO(b"not a real resume")
    bogus.name = "resume.txt"

    results = compare_resumes([bogus], "Python developer wanted")

    assert results == []
