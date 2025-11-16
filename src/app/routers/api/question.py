from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
    AnswerCreate,
    AnswerResponse,
    QuestionCreate,
    QuestionDetail,
    QuestionResponse,
)
from app.services import AnswerService, QuestionService
from core import db_helper
from users import User, current_user

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionResponse])
async def list_questions(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    return await QuestionService.list_questions(session)


@router.get("/{question_id}", response_model=QuestionDetail)
async def get_question(
    question_id: int, session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    try:
        question = await QuestionService.get_question(question_id, session)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return question


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    data: QuestionCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    return await QuestionService.create_question(data, session)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    try:
        await QuestionService.delete_question(question_id, session)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{question_id}/answers",
    response_model=AnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_answer(
    question_id: int,
    data: AnswerCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    user: User = Depends(current_user),
):
    try:
        answer = await AnswerService.create_answer(question_id, data, session, user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return answer
