from uuid import UUID

from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession

from app.app import app
from core import Answer, Question, db_helper
from users import User


def override_db_session(session: AsyncSession) -> None:
    """Override db session dependencies"""

    def override_get_scoped_session():
        return session

    async def override_session_dependency():
        yield session

    app.dependency_overrides[db_helper.get_scoped_session] = override_get_scoped_session
    app.dependency_overrides[db_helper.session_dependency] = override_session_dependency


async def create_user(email: str, password: str, session: AsyncSession) -> User:
    hashed_password = PasswordHelper().hash(password)
    user = User(email=email, hashed_password=hashed_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_question(text: str, session: AsyncSession) -> Question:
    question = Question(text=text)
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


async def create_answer(
    text: str, question_id: int, user_id: UUID, session: AsyncSession
) -> Answer:
    answer = Answer(
        text=text,
        question_id=question_id,
        user_id=user_id,
    )
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return answer
