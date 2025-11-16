from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.mixins import DBTextDateMixin
from .base import Base

if TYPE_CHECKING:
    from .answer import Answer


class Question(DBTextDateMixin, Base):
    """Model representing a question"""

    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="question", lazy="selectin"
    )
