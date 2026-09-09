"""
诊断路由模块
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

from app.core.database import neo4j_driver
from app.services.knowledge_graph import KnowledgeGraphService
from app.services.bkt import BKTService
from app.services.diagnostic import DiagnosticService

router = APIRouter()


class DiagnosticRequest(BaseModel):
    """诊断请求"""
    learner_id: str
    knowledge_state: Dict[str, float]
    error_history: Optional[List[Dict]] = None


class DiagnosticResponse(BaseModel):
    """诊断响应"""
    learner_id: str
    weak_points: List[Dict]
    overall_mastery: float
    recommendations: List[str]
    error_summary: Dict[str, int]
    category_mastery: Dict[str, float]


@router.post("/analyze", response_model=DiagnosticResponse)
async def analyze_diagnostic(request: DiagnosticRequest):
    """分析学习者薄弱点"""
    # 创建服务实例
    kg_service = KnowledgeGraphService(neo4j_driver)
    bkt_service = BKTService()
    diagnostic_service = DiagnosticService(kg_service, bkt_service)
    
    # 生成诊断报告
    report = await diagnostic_service.generate_diagnostic_report(
        learner_id=request.learner_id,
        learner_state=request.knowledge_state,
        error_history=request.error_history,
    )
    
    return DiagnosticResponse(
        learner_id=report.learner_id,
        weak_points=[
            {
                "knowledge_point_id": wp.knowledge_point_id,
                "name": wp.name,
                "level": wp.level,
                "category": wp.category,
                "mastery": wp.mastery,
                "confidence": wp.confidence,
                "root_cause": wp.root_cause,
            }
            for wp in report.weak_points
        ],
        overall_mastery=report.overall_mastery,
        recommendations=report.recommendations,
        error_summary=report.error_summary,
        category_mastery=report.category_mastery,
    )


@router.post("/root-cause")
async def root_cause_analysis(
    error_kp_id: str,
    knowledge_state: Dict[str, float],
):
    """根因分析"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    bkt_service = BKTService()
    diagnostic_service = DiagnosticService(kg_service, bkt_service)
    
    root_causes = await diagnostic_service.root_cause_analysis(
        error_kp_id=error_kp_id,
        learner_state=knowledge_state,
    )
    
    return {"root_causes": root_causes}
