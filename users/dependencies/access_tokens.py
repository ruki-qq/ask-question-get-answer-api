from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from core import db_helper
from core.models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_dependency),
    ]
):
    yield AccessToken.get_db(session=session)
