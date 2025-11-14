from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from users.dependencies.fastapi_users import current_user
from users.models import User
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionDetail
from app.schemas.answer import AnswerResponse
from core import Question, db_helper

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionResponse])
async def list_questions(session: AsyncSession = Depends(db_helper.session_dependency)):
    result = await session.execute(select(Question))
    return result.scalars().all()


@router.get("/my", response_model=list[QuestionResponse])
async def my_questions(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
):
    result = await session.execute(
        select(Question).where(Question.user_id == str(user.id))
    )
    return result.scalars().all()


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    data: QuestionCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
):
    question = Question(text=data.text, user_id=str(user.id))
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


@router.get("/{id}", response_model=QuestionDetail)
async def get_question(
    id: int, session: AsyncSession = Depends(db_helper.session_dependency)
):
    result = await session.execute(
        select(Question).where(Question.id == id).options(selectinload(Question.answer))
    )
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionDetail(
        id=question.id,
        text=question.text,
        created_at=question.created_at,
        answers=[
            AnswerResponse(
                id=ans.id,
                text=ans.text,
                user_id=ans.user_id,
                question_id=ans.question_id,
                created_at=ans.created_at,
            )
            for ans in question.answer
        ],
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(current_user),
):
    question = await session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    if question.user_id != str(user.id):
        raise HTTPException(
            status_code=403, detail="You can delete only your own questions"
        )
    await session.delete(question)
    await session.commit()
    return None
