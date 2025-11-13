from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..mixins import DBTextDateMixin


class Answer(DBTextDateMixin, Base):
    """Model representing an answer to a question"""

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )

    question = relationship("Question", back_populates="answer", lazy="selectin")
