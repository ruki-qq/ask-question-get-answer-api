from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.mixins import DBTextDateMixin
from .base import Base

if TYPE_CHECKING:
    from .question import Question


class Answer(DBTextDateMixin, Base):
    """Model representing an answer to a question"""

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    question: Mapped["Question"] = relationship(
        "Question", back_populates="answers", lazy="joined"
    )
