from typing import List

from pydantic import BaseModel


class BulletRewrite(BaseModel):
    original: str
    improved: str
    reason: str


class ResumeRewrite(BaseModel):
    rewrites: List[BulletRewrite]
    general_advice: List[str]
