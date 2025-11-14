from sqlalchemy.orm import relationship, Mapped, mapped_column

from .base import Base
from ..mixins import DBTextDateMixin


class Question(DBTextDateMixin, Base):
    """Model representing a question"""

    user_id: Mapped[str] = mapped_column()

    answer = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete",
        passive_deletes=True,
        lazy="selectin",
    )
