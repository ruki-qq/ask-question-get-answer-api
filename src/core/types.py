from typing import TypeVar

from core.models import Base

BaseChild = TypeVar("BaseChild", bound=Base)
