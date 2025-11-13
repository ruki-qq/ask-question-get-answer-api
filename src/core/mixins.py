from datetime import datetime
from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now


class DBTextDateMixin:
    """Mixin for models with text and created_at fields"""

    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=now())
