from fastapi import APIRouter

from core.config import settings
from users.dependencies.backend import auth_backend
from users.dependencies.fastapi_users import fastapi_users
from users.schemas import UserCreate, UserRead

router = APIRouter(prefix=settings.auth_prefix, tags=["auth"])


router.include_router(
    router=fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(router=fastapi_users.get_reset_password_router())
