from pydantic import BaseModel
from typing import List


class Criterion(BaseModel):
    name: str
    weight: float


class OptionScore(BaseModel):
    option: str
    scores: List[float]


class DecisionRequest(BaseModel):
    title: str
    options: List[str]
    criteria: List[Criterion]
    option_scores: List[OptionScore]