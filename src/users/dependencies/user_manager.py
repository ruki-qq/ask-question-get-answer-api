from uuid import UUID
from typing import Annotated, Optional, TYPE_CHECKING

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from core import settings
from users.models import User
from .users import get_users_db

if TYPE_CHECKING:
    from fastapi import Request
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.jwt.reset_password_token_secret
    verification_token_secret = settings.jwt.verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(
    users_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_users_db),
    ],
):
    yield UserManager(users_db)
