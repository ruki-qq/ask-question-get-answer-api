from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    text: str = Field(..., min_length=1)


class AnswerCreate(AnswerBase):
    pass


class AnswerResponse(AnswerBase):
    id: int
    question_id: int
    user_id: UUID
    created_at: datetime
