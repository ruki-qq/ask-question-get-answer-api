from datetime import datetime

from pydantic import BaseModel

from .answer import AnswerResponse


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class QuestionDetail(QuestionResponse):
    answers: list[AnswerResponse] = []
