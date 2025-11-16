from fastapi import APIRouter

from core.config import settings
from users.dependencies import auth_backend, fastapi_users
from users.schemas import UserCreate, UserRead

router = APIRouter(prefix=settings.auth_prefix, tags=["auth"])

router.include_router(
    router=fastapi_users.get_auth_router(auth_backend, requires_verification=False),
)

router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate),
)
