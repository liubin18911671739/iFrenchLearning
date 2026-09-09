from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_postgres_session
from app.schemas.learner import LearnerCreate, LearnerResponse

router = APIRouter()


@router.get("/", response_model=list[LearnerResponse])
async def get_learners(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_postgres_session),
):
    """获取学习者列表"""
    # TODO: 实现学习者查询
    return []


@router.post("/", response_model=LearnerResponse)
async def create_learner(
    learner: LearnerCreate,
    db: AsyncSession = Depends(get_postgres_session),
):
    """创建学习者"""
    # TODO: 实现学习者创建
    return LearnerResponse(id="new-learner", **learner.model_dump())


@router.get("/{learner_id}/state")
async def get_learner_state(learner_id: str):
    """获取学习者知识状态"""
    # TODO: 实现学习者状态查询
    return {
        "learner_id": learner_id,
        "knowledge_state": {},
        "last_updated": None,
    }
