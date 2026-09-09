"""
知识图谱路由模块
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.core.database import neo4j_driver
from app.services.knowledge_graph import KnowledgeGraphService

router = APIRouter()


@router.get("/")
async def get_knowledge_graph(
    level: Optional[str] = Query(None, description="CEFR等级筛选"),
    max_nodes: int = Query(100, description="最大节点数"),
):
    """获取知识图谱数据"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    data = await kg_service.get_knowledge_graph_for_visualization(
        level=level,
        max_nodes=max_nodes,
    )
    return data


@router.get("/stats")
async def get_statistics():
    """获取知识图谱统计信息"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    stats = await kg_service.get_statistics()
    return stats


@router.get("/{node_id}")
async def get_knowledge_point(node_id: str):
    """获取知识点详情"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    kp = await kg_service.get_knowledge_point_by_id(node_id)
    if not kp:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Knowledge point not found")
    return kp


@router.get("/{node_id}/prerequisites")
async def get_prerequisites(node_id: str):
    """获取前置知识"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    prereqs = await kg_service.get_prerequisites(node_id)
    return {"node_id": node_id, "prerequisites": prereqs}


@router.get("/{node_id}/dependents")
async def get_dependents(node_id: str):
    """获取后续知识"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    dependents = await kg_service.get_dependents(node_id)
    return {"node_id": node_id, "dependents": dependents}


@router.get("/path/{current}/{target}")
async def find_learning_path(current: str, target: str):
    """查找学习路径"""
    kg_service = KnowledgeGraphService(neo4j_driver)
    path = await kg_service.find_learning_path(current, target)
    return {
        "current": current,
        "target": target,
        "path": path,
    }
