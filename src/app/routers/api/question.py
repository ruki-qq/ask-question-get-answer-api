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
from core import db_helper, get_logger
from users import User, current_user

logger = get_logger(__name__)
router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionResponse])
async def list_questions(session: AsyncSession = Depends(db_helper.get_scoped_session)):
    logger.info("Getting list of all questions")
    logger.debug(
        f"Running QuestionService.list_questions method with session = {session}"
    )
    return await QuestionService.list_questions(session)


@router.get("/{question_id}", response_model=QuestionDetail)
async def get_question(
    question_id: int, session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    logger.info(f"Getting a question with id: {question_id}")
    try:
        logger.debug(
            f"Running QuestionService.get_question method with question id: {question_id} and session: {session}"
        )
        question = await QuestionService.get_question(question_id, session)
    except KeyError as e:
        logger.error(f"QuestionService.get_question method returned a KeyError: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    return question


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    data: QuestionCreate,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    logger.info("Creating a question with given data")
    logger.debug(
        f"Running QuestionService.create_question method with data = {data} and session = {session}"
    )
    return await QuestionService.create_question(data, session)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
):
    logger.info(f"Deleting a question with id: {question_id}")
    try:
        logger.debug(
            f"Running QuestionService.delete_question method with question_id = {question_id} and session = {session}"
        )
        await QuestionService.delete_question(question_id, session)
    except KeyError as e:
        logger.error(f"QuestionService.delete_question method returned a KeyError: {e}")
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
    logger.info(f"Creating an answer to question with id: {question_id}")
    try:
        logger.debug(
            f"Running AnswerService.create_answer method with question_id = {question_id}"
            f", data = {data}, session = {session} and user = {user}"
        )
        answer = await AnswerService.create_answer(question_id, data, session, user)
    except ValueError as e:
        logger.error(f"AnswerService.create_answer method returned a ValueError: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    except KeyError as e:
        logger.error(f"AnswerService.create_answer method returned a KeyError: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    return answer
