from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class KnowledgePointBase(BaseModel):
    """知识点基础模型"""
    id: str = Field(..., description="知识点ID")
    name: str = Field(..., description="知识点名称")
    level: str = Field(..., description="难度等级: A1/A2/B1/B2")
    category: str = Field(..., description="分类: vocabulary/grammar/verb_conjugation/accord")


class KnowledgePointResponse(KnowledgePointBase):
    """知识点响应"""
    description: Optional[str] = Field(default=None, description="描述")
    prerequisites: List[str] = Field(default_factory=list, description="前置知识点ID列表")

    class Config:
        from_attributes = True


class KnowledgeGraphResponse(BaseModel):
    """知识图谱响应"""
    nodes: List[KnowledgePointResponse] = Field(default_factory=list, description="节点列表")
    edges: List[dict] = Field(default_factory=list, description="边列表")


class LearningPathResponse(BaseModel):
    """学习路径响应"""
    current: str = Field(..., description="当前知识点ID")
    target: str = Field(..., description="目标知识点ID")
    path: List[str] = Field(default_factory=list, description="学习路径")
    recommendations: List[dict] = Field(default_factory=list, description="推荐内容")
