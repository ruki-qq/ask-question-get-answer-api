from datetime import datetime

from pydantic import BaseModel


class QuestionBase(BaseModel):
    text: str
    created_at: datetime
    user_id: int


class AnswerCreate(QuestionBase):
    pass


class AnswerUpdate(QuestionBase):
    pass


class Answer(QuestionBase):
    id: int
