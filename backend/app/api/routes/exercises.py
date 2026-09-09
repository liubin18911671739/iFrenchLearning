"""
练习路由模块
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Dict, List, Optional

from app.core.database import neo4j_driver
from app.services.knowledge_graph import KnowledgeGraphService
from app.services.bkt import BKTService
from app.services.recommendation import RecommendationEngine

router = APIRouter()


class RecommendRequest(BaseModel):
    """推荐请求"""
    learner_id: str
    knowledge_state: Dict[str, float]
    target_level: str = "B1"
    n_recommendations: int = 5


class SubmitExerciseRequest(BaseModel):
    """提交练习请求"""
    learner_id: str
    exercise_id: str
    knowledge_point_id: str
    correct: bool
    response_time_ms: Optional[int] = None


class UpdateMasteryRequest(BaseModel):
    """更新掌握度请求"""
    skill_id: str
    current_mastery: float
    correct: bool


@router.post("/recommend")
async def get_recommendations(request: RecommendRequest):
    """获取推荐练习"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    bkt_service = BKTService()
    engine = RecommendationEngine(kg_service, bkt_service)
    
    recommendations = await engine.get_recommendations(
        learner_state=request.knowledge_state,
        target_level=request.target_level,
        n_recommendations=request.n_recommendations,
    )
    
    return {
        "learner_id": request.learner_id,
        "recommendations": [
            {
                "knowledge_point_id": rec.knowledge_point_id,
                "name": rec.name,
                "level": rec.level,
                "category": rec.category,
                "reason": rec.reason,
                "score": rec.score,
            }
            for rec in recommendations
        ],
    }


@router.post("/learning-path")
async def get_learning_path(
    knowledge_state: Dict[str, float],
    target_kp_id: str,
):
    """获取学习路径"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    bkt_service = BKTService()
    engine = RecommendationEngine(kg_service, bkt_service)
    
    path = await engine.get_learning_path_recommendation(
        learner_state=knowledge_state,
        target_kp_id=target_kp_id,
    )
    
    return {
        "target": target_kp_id,
        "path": [
            {
                "knowledge_point_id": rec.knowledge_point_id,
                "name": rec.name,
                "reason": rec.reason,
            }
            for rec in path
        ],
    }


@router.post("/submit")
async def submit_exercise(request: SubmitExerciseRequest):
    """提交练习答案"""
    bkt_service = BKTService()
    
    # 更新掌握度
    new_mastery = bkt_service.update_mastery(
        current_mastery=0.5,  # 实际应从数据库获取
        correct=request.correct,
        skill_id=request.knowledge_point_id,
    )
    
    return {
        "exercise_id": request.exercise_id,
        "correct": request.correct,
        "new_mastery": new_mastery,
        "mastery_level": bkt_service.get_mastery_level(new_mastery),
    }


@router.post("/update-mastery")
async def update_mastery(request: UpdateMasteryRequest):
    """更新掌握度"""
    bkt_service = BKTService()
    
    new_mastery = bkt_service.update_mastery(
        current_mastery=request.current_mastery,
        correct=request.correct,
        skill_id=request.skill_id,
    )
    
    return {
        "skill_id": request.skill_id,
        "previous_mastery": request.current_mastery,
        "new_mastery": new_mastery,
        "correct": request.correct,
        "mastery_level": bkt_service.get_mastery_level(new_mastery),
    }
