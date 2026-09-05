from datetime import datetime

from fpdf import FPDF


def _safe(text) -> str:
    """
    fpdf2's built-in core fonts (Helvetica) only support the
    latin-1 character set. Resume text or AI output can contain
    smart quotes, emoji, or other unicode -- replace anything
    unsupported instead of crashing the report generation.
    """
    if text is None:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 41, 59)
        self.cell(0, 12, "ResumeIQ - Analysis Report", ln=True, align="C")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(
            0, 6,
            datetime.now().strftime("Generated on %B %d, %Y at %I:%M %p"),
            ln=True, align="C",
        )
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.ln(2)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(30, 41, 59)
        self.cell(0, 9, _safe(title), ln=True)

        self.set_draw_color(200, 200, 200)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(3)

    def body_text(self, text, bullet=False):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(20, 20, 20)
        prefix = "- " if bullet else ""
        self.multi_cell(0, 6, _safe(f"{prefix}{text}"))
        self.ln(1)


def generate_report_pdf(
    ats_score,
    skill_match_percentage,
    matched_skills,
    missing_skills,
    analysis=None,
    interview_prep=None,
    ats_breakdown=None,
    content_similarity=None,
    rewrite=None,
    cover_letter=None,
) -> bytes:
    """
    Build a downloadable PDF summary of the resume analysis
    (rule-based ATS score + breakdown, skill match, content
    similarity, AI insights, rewrite suggestions, interview prep,
    and cover letter, where available).

    Returns raw PDF bytes suitable for st.download_button.
    """
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ---------- Score Overview ----------
    pdf.section_title("Score Overview")
    pdf.body_text(f"Rule-Based ATS Score: {ats_score}/100")
    pdf.body_text(f"Job Description Skill Match: {skill_match_percentage}%")

    if content_similarity is not None:
        pdf.body_text(f"Content Similarity (TF-IDF): {content_similarity}%")

    if analysis is not None:
        pdf.body_text(f"AI ATS Score: {analysis.ats_score}/100")

    if ats_breakdown:
        pdf.section_title("ATS Score Breakdown")
        for category in ats_breakdown.values():
            pdf.body_text(
                f"{category['label']}: {category['score']:.0f}/{category['max']} "
                f"({category.get('detail', '')})",
                bullet=True,
            )

    # ---------- Skills ----------
    pdf.section_title("Matched Skills")
    pdf.body_text(", ".join(matched_skills) if matched_skills else "None found.")

    pdf.section_title("Missing Skills (from Job Description)")
    pdf.body_text(
        ", ".join(missing_skills) if missing_skills else "None - great coverage!"
    )

    # ---------- AI Insights ----------
    if analysis is not None:
        pdf.section_title("Professional Summary")
        pdf.body_text(analysis.professional_summary or "Not available.")

        pdf.section_title("Strengths")
        if analysis.strengths:
            for item in analysis.strengths:
                pdf.body_text(item, bullet=True)
        else:
            pdf.body_text("None listed.")

        pdf.section_title("Weaknesses")
        if analysis.weaknesses:
            for item in analysis.weaknesses:
                pdf.body_text(item, bullet=True)
        else:
            pdf.body_text("None listed.")

        pdf.section_title("Suggestions")
        if analysis.suggestions:
            for item in analysis.suggestions:
                pdf.body_text(item, bullet=True)
        else:
            pdf.body_text("None listed.")
    else:
        pdf.section_title("AI Insights")
        pdf.body_text(
            "AI analysis was not available for this report "
            "(check that OPENROUTER_API_KEY is configured)."
        )

    # ---------- Rewrite Suggestions ----------
    if rewrite is not None:
        pdf.add_page()
        pdf.section_title("Resume Rewrite Suggestions")

        for i, item in enumerate(rewrite.rewrites, start=1):
            pdf.body_text(f"{i}. Original: {item.original}")
            pdf.body_text(f"Improved: {item.improved}", bullet=True)
            pdf.body_text(f"Why: {item.reason}", bullet=True)

        if rewrite.general_advice:
            pdf.section_title("General Resume Advice")
            for advice in rewrite.general_advice:
                pdf.body_text(advice, bullet=True)

    # ---------- Interview Prep ----------
    if interview_prep is not None:
        pdf.add_page()
        pdf.section_title("Interview Preparation")

        for i, q in enumerate(interview_prep.questions, start=1):
            pdf.body_text(f"{i}. [{q.category}] {q.question}")
            pdf.body_text(f"Suggested answer: {q.suggested_answer}", bullet=True)

        if interview_prep.tips:
            pdf.section_title("Interview Tips For This Role")
            for tip in interview_prep.tips:
                pdf.body_text(tip, bullet=True)

    # ---------- Cover Letter ----------
    if cover_letter is not None:
        pdf.add_page()
        pdf.section_title("Cover Letter")
        pdf.body_text(cover_letter.cover_letter)

    return bytes(pdf.output())
