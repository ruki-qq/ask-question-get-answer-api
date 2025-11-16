from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import AnswerResponse
from app.services import AnswerService
from core import db_helper, get_logger
from users import User, current_user

logger = get_logger(__name__)
router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=AnswerResponse)
async def get_answer(
    answer_id: int, session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    logger.info(f"Getting answer with id {answer_id}")
    try:
        logger.debug("Running AnswerService.get_answer method")
        answer = await AnswerService.get_answer(answer_id, session)
    except KeyError as e:
        logger.error(f"AnswerService.get_answer method returned a KeyError: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: int,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    user: User = Depends(current_user),
):
    logger.info(f"Deleting answer with id {answer_id}")
    try:
        logger.debug("Running AnswerService.delete_answer method")
        await AnswerService.delete_answer(answer_id, session, user)
    except KeyError as e:
        logger.error(f"AnswerService.delete_answer method returned a KeyError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except AssertionError as e:
        logger.error(
            f"AnswerService.delete_answer method returned an AssertionError: {e}"
        )
        raise HTTPException(status_code=403, detail=str(e))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
