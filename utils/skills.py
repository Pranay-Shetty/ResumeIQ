import re

# ==========================================================
# Skill Taxonomy
# ==========================================================
# Organized by category purely for readability/maintenance.
# extract_skills() flattens these into a single lookup so
# matching behavior (and the public API) is unchanged.
# ==========================================================

SKILL_CATEGORIES = {
    "Programming Languages": [
        # NOTE: bare single-letter/common-word tokens (e.g. "c", "r", "go")
        # are deliberately excluded -- they false-positive match ordinary
        # text like lettered lists "(a) (b) (c)" or "go above and beyond".
        # "golang", "c++", "c#" are unambiguous enough to keep.
        "python", "java", "javascript", "typescript", "c++", "c#",
        "golang", "rust", "kotlin", "swift", "php", "ruby", "scala",
        "matlab", "bash", "shell scripting", "sql", "html", "css",
    ],
    "Frameworks & Libraries": [
        "streamlit", "fastapi", "flask", "django", "react", "react.js",
        "next.js", "vue", "angular", "node.js", "express.js", "spring",
        "spring boot", ".net", "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch", "keras", "opencv", "matplotlib",
        "seaborn", "plotly", "langchain", "llamaindex",
    ],
    "AI / ML / Data": [
        "machine learning", "deep learning", "nlp", "computer vision",
        "generative ai", "llm", "rag", "prompt engineering",
        "data analysis", "data engineering", "data science",
        "data visualization", "etl", "feature engineering",
        "model deployment", "mlops", "statistics", "a/b testing",
        "openai", "hugging face",
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "ansible", "jenkins", "ci/cd", "github actions", "linux",
        "nginx", "serverless", "cloudformation",
    ],
    "Databases": [
        "mysql", "postgresql", "mongodb", "redis", "sqlite",
        "oracle", "elasticsearch", "dynamodb", "firebase",
        "power bi", "tableau", "excel",
    ],
    "Tools & Platforms": [
        "git", "github", "gitlab", "jira", "confluence", "postman",
        "figma", "vs code", "slack", "notion",
    ],
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "project management", "agile", "scrum",
        "time management", "collaboration", "stakeholder management",
        "mentoring", "adaptability",
    ],
}

# Flattened, de-duplicated list used for matching.
COMMON_SKILLS = sorted(
    {skill for skills in SKILL_CATEGORIES.values() for skill in skills}
)

# A few skills contain characters (like "c++", "c#", ".net") that need
# custom word-boundary handling since \b doesn't work around them.
_SPECIAL_BOUNDARY_SKILLS = {"c++", "c#", ".net"}

# Skills whose .title()-cased form looks wrong (e.g. "Node.Js",
# "Ci/Cd") get an explicit display name instead.
_DISPLAY_OVERRIDES = {
    "c++": "C++",
    "c#": "C#",
    ".net": ".NET",
    "node.js": "Node.js",
    "react.js": "React.js",
    "next.js": "Next.js",
    "express.js": "Express.js",
    "ci/cd": "CI/CD",
    "a/b testing": "A/B Testing",
    "nlp": "NLP",
    "llm": "LLM",
    "rag": "RAG",
    "etl": "ETL",
    "mlops": "MLOps",
    "aws": "AWS",
    "gcp": "GCP",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
    "vs code": "VS Code",
    "fastapi": "FastAPI",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "dynamodb": "DynamoDB",
    "github": "GitHub",
    "github actions": "GitHub Actions",
    "gitlab": "GitLab",
    "opencv": "OpenCV",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "scikit-learn",
    "power bi": "Power BI",
    "openai": "OpenAI",
    "hugging face": "Hugging Face",
    "langchain": "LangChain",
    "llamaindex": "LlamaIndex",
    "cloudformation": "CloudFormation",
    "generative ai": "Generative AI",
}


# When both a base skill and a more specific variant match the same
# mention (e.g. "React" and "React.js" both matching "React.js"), keep
# only the more specific one so the UI doesn't show the same
# technology twice. Deliberately an explicit allowlist rather than a
# generic substring rule -- a generic rule would wrongly drop "SQL"
# whenever "PostgreSQL" also matched, since "sql" is a literal
# substring of "postgresql" even though they're distinct skills.
_SUPERSEDED_BY = {
    "react": "react.js",
    "spring": "spring boot",
    "github": "github actions",
}


def _pattern_for(skill: str) -> str:
    if skill in _SPECIAL_BOUNDARY_SKILLS:
        # \b doesn't work around characters like "+", "#", "." since
        # they aren't word characters -- but excluding "." from the
        # boundary itself (as this used to) breaks the common case of
        # the skill sitting right at the end of a sentence, e.g.
        # "...experience with C#." A trailing/leading "." is normally
        # just punctuation, not part of the token, so only word
        # characters should block the match here.
        return r"(?<!\w){}(?!\w)".format(re.escape(skill))
    return r"\b" + re.escape(skill) + r"\b"


def _display_name(skill: str) -> str:
    return _DISPLAY_OVERRIDES.get(skill, skill.title())


def extract_skills(text: str):
    """
    Extract known skills from text using a curated taxonomy
    covering languages, frameworks, AI/ML, cloud, databases,
    tools, and soft skills.
    """
    if not text:
        return []

    text = text.lower()

    raw_found = set()

    for skill in COMMON_SKILLS:
        pattern = _pattern_for(skill)

        if re.search(pattern, text):
            raw_found.add(skill)

    for base, extended in _SUPERSEDED_BY.items():
        if base in raw_found and extended in raw_found:
            raw_found.discard(base)

    return sorted(_display_name(skill) for skill in raw_found)
