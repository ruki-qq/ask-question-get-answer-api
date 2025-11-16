from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import AnswerResponse
from app.services import AnswerService
from core import db_helper
from users import User, current_user

router = APIRouter(prefix="/answers", tags=["answers"])


@router.get("/{answer_id}", response_model=AnswerResponse)
async def get_answer(
    answer_id: int, session: AsyncSession = Depends(db_helper.get_scoped_session)
):
    try:
        answer = await AnswerService.get_answer(answer_id, session)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return answer


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(
    answer_id: int,
    session: AsyncSession = Depends(db_helper.get_scoped_session),
    user: User = Depends(current_user),
):
    try:
        await AnswerService.delete_answer(answer_id, session, user)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AssertionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
