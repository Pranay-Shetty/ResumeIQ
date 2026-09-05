import io

import fitz
from docx import Document as DocxDocument

from parser.pdf_parser import extract_pdf_text
from parser.docx_parser import extract_docx_text


def _make_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def _make_docx_bytes(paragraphs) -> bytes:
    doc = DocxDocument()
    for paragraph in paragraphs:
        doc.add_paragraph(paragraph)
    buffer = io.BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


def test_extract_pdf_text_reads_back_the_content():
    pdf_bytes = _make_pdf_bytes("Jane Doe Python Developer")
    uploaded = io.BytesIO(pdf_bytes)

    text = extract_pdf_text(uploaded)

    assert "Jane Doe" in text
    assert "Python Developer" in text


def test_extract_docx_text_reads_back_each_paragraph():
    docx_bytes = _make_docx_bytes(["Jane Doe", "Python Developer"])
    uploaded = io.BytesIO(docx_bytes)

    text = extract_docx_text(uploaded)

    assert "Jane Doe" in text
    assert "Python Developer" in text
