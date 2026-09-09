"""
API路由模块
"""

from fastapi import APIRouter

from app.api.routes import health, learners, knowledge_graph, exercises, diagnostics

api_router = APIRouter()

api_router.include_router(health.router, tags=["健康检查"])
api_router.include_router(learners.router, prefix="/learners", tags=["学习者"])
api_router.include_router(knowledge_graph.router, prefix="/knowledge-graph", tags=["知识图谱"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["练习"])
api_router.include_router(diagnostics.router, prefix="/diagnostics", tags=["诊断"])
