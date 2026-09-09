from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class LearnerBase(BaseModel):
    """学习者基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="学习者姓名")
    level: str = Field(default="A1", description="CEFR等级: A1/A2/B1/B2")


class LearnerCreate(LearnerBase):
    """创建学习者请求"""
    pass


class LearnerResponse(LearnerBase):
    """学习者响应"""
    id: str = Field(..., description="学习者ID")
    created_at: Optional[datetime] = Field(default=None, description="创建时间")

    class Config:
        from_attributes = True


class KnowledgeState(BaseModel):
    """知识状态模型"""
    knowledge_point_id: str = Field(..., description="知识点ID")
    mastery: float = Field(..., ge=0, le=1, description="掌握概率")
    last_practiced: Optional[datetime] = Field(default=None, description="最后练习时间")


class LearnerStateResponse(BaseModel):
    """学习者状态响应"""
    learner_id: str = Field(..., description="学习者ID")
    knowledge_state: Dict[str, KnowledgeState] = Field(default_factory=dict, description="知识状态")
    overall_mastery: float = Field(default=0.0, description="总体掌握度")
    last_updated: Optional[datetime] = Field(default=None, description="最后更新时间")
