from datetime import datetime

from pydantic import BaseModel


class AnswerBase(BaseModel):
    text: str
    user_id: str


class AnswerCreate(AnswerBase):
    pass


class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    created_at: datetime

    class Config:
        orm_mode = True
