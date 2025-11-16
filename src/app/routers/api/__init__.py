__all__ = ("router",)

from fastapi import APIRouter

from .answer import router as answer_router
from .question import router as question_router

router = APIRouter(prefix="/api", tags=["api"])
router.include_router(answer_router)
router.include_router(question_router)
