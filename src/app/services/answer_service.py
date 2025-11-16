from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import AnswerCreate
from core import Answer, Question
from users import User


class AnswerService:
    @staticmethod
    async def get_answer(answer_id: int, session: AsyncSession) -> type[Answer]:
        """Get an answer by id"""

        answer = await session.get(Answer, answer_id)

        if not answer:
            raise KeyError(f"Answer with id: {answer_id} not found")

        return answer

    @staticmethod
    async def create_answer(
        question_id: int, data: AnswerCreate, session: AsyncSession, user: User
    ) -> Answer:
        """Create an answer by id"""

        if not user:
            raise ValueError("Unauthorized")

        question = await session.get(Question, question_id)

        if not question:
            raise KeyError(f"Question with id: {question_id} not found")

        answer = Answer(text=data.text, user_id=user.id, question_id=question_id)
        session.add(answer)
        await session.commit()
        await session.refresh(answer)
        return answer

    @staticmethod
    async def delete_answer(
        answer_id: int,
        session: AsyncSession,
        user: User,
    ) -> None:
        """Delete an answer by id"""

        answer = await session.get(Answer, answer_id)

        if not answer:
            raise KeyError(f"Answer with id: {answer_id} not found")
        if answer.user_id != user.id:
            raise AssertionError("You can delete only your own answers")

        await session.delete(answer)
        await session.commit()
        return None
