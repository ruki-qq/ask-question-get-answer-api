from fastapi_users import FastAPIUsers

from core.types import UserIdType
from users.models import User

from .backend import auth_backend
from .user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
