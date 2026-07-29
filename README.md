# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that compares resumes against job descriptions and provides ATS scoring, skill-gap analysis, and AI-powered suggestions.

## 🚀 Features

- Upload PDF/DOCX resumes
- Resume text extraction
- Rule-based ATS compatibility score
- Skill-gap analysis across a 130+ skill taxonomy (languages, frameworks, cloud, databases, tools, soft skills)
- AI-powered resume analysis and improvement suggestions (via OpenRouter)
- Downloadable PDF analysis report

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenAI SDK (via OpenRouter)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)
- Plotly (skill-match chart)
- Pydantic (AI response validation)
- fpdf2 (PDF report generation)

## 📌 Project Status

✅ Feature-complete (v1.0) — core pipeline works end to end; ongoing polish and bug fixes.

## 📅 Roadmap

- [x] Project setup
- [x] Streamlit UI
- [x] Resume parsing
- [x] ATS scoring
- [x] AI suggestions
- [x] PDF report generation
- [ ] Cover letter generator
- [ ] Interview question generator
- [ ] Docker deployment

## ⚙️ Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=your_key_here
```

Run the app (must use `streamlit run`, not `python app.py`):

```bash
streamlit run app.py
```

## 📷 Screenshots

Coming soon.
