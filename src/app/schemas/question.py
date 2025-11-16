from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas import AnswerResponse


class QuestionBase(BaseModel):
    text: str = Field(..., min_length=1)


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime


class QuestionDetail(QuestionResponse):
    answers: list[AnswerResponse] = []
