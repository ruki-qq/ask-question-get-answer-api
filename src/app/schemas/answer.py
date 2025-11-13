from datetime import datetime

from pydantic import BaseModel


class AnswerBase(BaseModel):
    text: str
    created_at: datetime
    question_id: int
    user_id: int


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
