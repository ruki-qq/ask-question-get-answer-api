from os import getenv

from fastapi_users.authentication import JWTStrategy

from core import settings

SECRET = getenv("JWT_SECRET", "secret")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings.jwt.lifetime_seconds)
