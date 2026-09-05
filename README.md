# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that compares resumes against job descriptions and provides ATS scoring, skill-gap analysis, and AI-powered suggestions.

## 🚀 Features

- Upload PDF/DOCX resumes
- Resume text extraction
- Rule-based ATS compatibility score, broken down by category (keyword match, quantified achievements, resume length, contact info)
- Skill-gap analysis across a 130+ skill taxonomy (languages, frameworks, cloud, databases, tools, soft skills)
- TF-IDF content similarity score between resume and job description, as a lexical complement to exact skill matching
- AI-powered resume analysis and improvement suggestions (via OpenRouter)
- AI-powered resume bullet-point rewrite suggestions, tailored to the job description
- AI-generated, tone-adjustable cover letter, editable before download
- AI-generated interview prep kit (tailored questions + suggested answers + role tips)
- Compare multiple resumes against the same job description side by side, ranked by ATS score
- Downloadable PDF analysis report

## 🛠️ Tech Stack

- Python
- Streamlit
- OpenAI SDK (via OpenRouter)
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)
- Plotly (skill-match donut chart, resume comparison bar chart)
- scikit-learn (TF-IDF content similarity)
- Pandas (resume comparison table)
- Pydantic (AI response validation)
- fpdf2 (PDF report generation)

## 📌 Project Status

✅ Feature-complete (v1.1) — core pipeline plus rewrite suggestions, cover letter generation, and multi-resume comparison; ongoing polish and bug fixes.

## 📅 Roadmap

- [x] Project setup
- [x] Streamlit UI
- [x] Resume parsing
- [x] ATS scoring (with category breakdown)
- [x] AI suggestions
- [x] PDF report generation
- [x] Cover letter generator
- [x] Interview question generator
- [x] Resume rewrite suggestions
- [x] Multi-resume comparison
- [ ] Automated test suite
- [ ] CI (GitHub Actions)
- [ ] Docker deployment
- [ ] Live deployment (Streamlit Community Cloud)

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

