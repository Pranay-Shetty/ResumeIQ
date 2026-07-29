from typing import List

from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    category: str
    question: str
    suggested_answer: str


class InterviewPrep(BaseModel):
    questions: List[InterviewQuestion]
    tips: List[str]
