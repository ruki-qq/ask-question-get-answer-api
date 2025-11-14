from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Question, Answer
from app.schemas.answer import AnswerCreate, AnswerResponse
from core.db_helper import db_helper
from users.dependencies.fastapi_users import current_user
from users.models import User

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    question_id: int,
    data: AnswerCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
):
    question = await session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer = Answer(text=data.text, user_id=str(user.id), question_id=question_id)
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return answer


@router.get("/answers/{answer_id}", response_model=AnswerResponse)
async def get_answer(
    answer_id: int, session: AsyncSession = Depends(db_helper.session_dependency)
):
    answer = await session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
):
    answer = await session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    if answer.user_id != str(user.id):
        raise HTTPException(
            status_code=403, detail="You can delete only your own answers"
        )
    await session.delete(answer)
    await session.commit()
    return None
