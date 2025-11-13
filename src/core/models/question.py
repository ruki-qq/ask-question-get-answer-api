from sqlalchemy.orm import relationship

from .base import Base
from ..mixins import DBTextDateMixin


class Question(DBTextDateMixin, Base):
    """Model representing a question"""

    answer = relationship(
        "Reservation",
        back_populates="question",
        cascade="all, delete",
        passive_deletes=True,
        lazy="selectin",
    )
