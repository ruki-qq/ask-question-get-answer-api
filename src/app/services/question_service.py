from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import QuestionCreate
from core import Question


class QuestionService:
    @staticmethod
    async def list_questions(session: AsyncSession) -> Sequence[Question]:
        """List all questions"""

        questions = await session.execute(select(Question))
        return questions.scalars().all()

    @staticmethod
    async def get_question(question_id: int, session: AsyncSession) -> type[Question]:
        """Get a question by id"""

        question = await session.get(Question, question_id)

        if not question:
            raise KeyError(f"Question with id: {question_id} not found")

        return question

    @staticmethod
    async def create_question(data: QuestionCreate, session: AsyncSession) -> Question:
        """Create a new question"""

        question = Question(text=data.text)
        session.add(question)
        await session.commit()
        await session.refresh(question)
        return question

    @staticmethod
    async def delete_question(question_id: int, session: AsyncSession) -> None:
        """Delete a question by id"""

        question = await session.get(Question, question_id)

        if not question:
            raise KeyError(f"Question with id: {question_id} not found")

        await session.delete(question)
        await session.commit()
        return None
