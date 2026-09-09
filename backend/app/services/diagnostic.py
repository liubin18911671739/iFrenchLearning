"""
薄弱点诊断模块
通过知识图谱推理，从表面错误定位根本薄弱知识点
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from .knowledge_graph import KnowledgeGraphService
from .bkt import BKTService


@dataclass
class WeakPoint:
    """薄弱知识点"""
    knowledge_point_id: str
    name: str
    level: str
    category: str
    mastery: float
    confidence: float
    root_cause: bool = False
    related_errors: Optional[List[str]] = None

    def __post_init__(self):
        if self.related_errors is None:
            self.related_errors = []


@dataclass
class DiagnosticReport:
    """诊断报告"""
    learner_id: str
    weak_points: List[WeakPoint]
    overall_mastery: float
    recommendations: List[str]
    error_summary: Dict[str, int]
    category_mastery: Dict[str, float]


class DiagnosticService:
    """薄弱点诊断服务"""

    def __init__(
        self,
        kg_service: KnowledgeGraphService,
        bkt_service: BKTService,
    ):
        self.kg = kg_service
        self.bkt = bkt_service

    async def analyze_weak_points(
        self,
        learner_state: Dict[str, float],
        error_history: Optional[List[Dict]] = None,
    ) -> List[WeakPoint]:
        """
        分析学习者的薄弱知识点
        
        Args:
            learner_state: 学习者知识状态 {skill_id: mastery}
            error_history: 错误历史记录
            
        Returns:
            薄弱知识点列表
        """
        weak_points = []
        
        # 分析所有知识点
        for kp_id, mastery in learner_state.items():
            if mastery < 0.6:  # 薄弱阈值
                kp = await self.kg.get_knowledge_point_by_id(kp_id)
                if not kp:
                    continue
                
                # 计算置信度
                confidence = 1.0 - mastery
                
                # 检查是否是根本原因
                root_cause = await self._check_root_cause(kp_id, learner_state)
                
                weak_points.append(WeakPoint(
                    knowledge_point_id=kp_id,
                    name=kp["name"],
                    level=kp["level"],
                    category=kp["category"],
                    mastery=mastery,
                    confidence=confidence,
                    root_cause=root_cause,
                ))
        
        # 按掌握度排序（最弱的优先）
        weak_points.sort(key=lambda x: x.mastery)
        
        return weak_points

    async def _check_root_cause(
        self,
        kp_id: str,
        learner_state: Dict[str, float],
    ) -> bool:
        """
        检查某知识点是否是其他知识点薄弱的根本原因
        
        如果某知识点被多个薄弱知识点依赖，则可能是根本原因
        """
        # 获取依赖此知识点的后续知识点
        dependents = await self.kg.get_dependents(kp_id)
        
        if not dependents:
            return False
        
        # 统计依赖此知识点的薄弱知识点数量
        dependent_weak_count = sum(
            1 for dep in dependents
            if learner_state.get(dep["knowledge_point"]["id"], 0) < 0.6
        )
        
        # 如果超过一半的依赖知识点都是薄弱的，则认为是根本原因
        return dependent_weak_count > len(dependents) / 2

    async def root_cause_analysis(
        self,
        error_kp_id: str,
        learner_state: Dict[str, float],
    ) -> List[Dict]:
        """
        根因分析：从错误类型回溯到根本薄弱知识点
        
        Args:
            error_kp_id: 出错的知识点ID
            learner_state: 学习者知识状态
            
        Returns:
            根本原因列表
        """
        root_causes = []
        
        # 获取该知识点的所有前置知识
        prereqs = await self.kg.get_prerequisites(error_kp_id)
        
        for prereq in prereqs:
            prereq_id = prereq["knowledge_point"]["id"]
            mastery = learner_state.get(prereq_id, 0)
            
            if mastery < 0.6:
                root_causes.append({
                    "knowledge_point_id": prereq_id,
                    "name": prereq["knowledge_point"]["name"],
                    "mastery": mastery,
                    "confidence": 1.0 - mastery,
                    "depth": 1,
                })
                
                # 递归检查更深层的前置知识
                deeper_causes = await self._recursive_root_cause(
                    prereq_id, learner_state, depth=1, max_depth=3
                )
                root_causes.extend(deeper_causes)
        
        # 去重并按置信度排序
        seen_ids = set()
        unique_causes = []
        for cause in root_causes:
            if cause["knowledge_point_id"] not in seen_ids:
                seen_ids.add(cause["knowledge_point_id"])
                unique_causes.append(cause)
        
        unique_causes.sort(key=lambda x: x["confidence"], reverse=True)
        
        return unique_causes

    async def _recursive_root_cause(
        self,
        kp_id: str,
        learner_state: Dict[str, float],
        depth: int,
        max_depth: int,
    ) -> List[Dict]:
        """递归查找根因"""
        if depth >= max_depth:
            return []
        
        causes = []
        prereqs = await self.kg.get_prerequisites(kp_id)
        
        for prereq in prereqs:
            prereq_id = prereq["knowledge_point"]["id"]
            mastery = learner_state.get(prereq_id, 0)
            
            if mastery < 0.6:
                causes.append({
                    "knowledge_point_id": prereq_id,
                    "name": prereq["knowledge_point"]["name"],
                    "mastery": mastery,
                    "confidence": (1.0 - mastery) * (0.8 ** depth),
                    "depth": depth,
                })
                
                # 继续递归
                deeper_causes = await self._recursive_root_cause(
                    prereq_id, learner_state, depth + 1, max_depth
                )
                causes.extend(deeper_causes)
        
        return causes

    async def generate_diagnostic_report(
        self,
        learner_id: str,
        learner_state: Dict[str, float],
        error_history: Optional[List[Dict]] = None,
    ) -> DiagnosticReport:
        """
        生成诊断报告
        
        Args:
            learner_id: 学习者ID
            learner_state: 学习者知识状态
            error_history: 错误历史记录
            
        Returns:
            诊断报告
        """
        # 分析薄弱点
        weak_points = await self.analyze_weak_points(learner_state, error_history)
        
        # 计算总体掌握度
        if learner_state:
            overall_mastery = sum(learner_state.values()) / len(learner_state)
        else:
            overall_mastery = 0.0
        
        # 按类别统计掌握度
        category_mastery = await self._calculate_category_mastery(learner_state)
        
        # 生成错误摘要
        error_summary = {}
        if error_history:
            for error in error_history:
                category = error.get("category", "unknown")
                error_summary[category] = error_summary.get(category, 0) + 1
        
        # 生成建议
        recommendations = await self._generate_recommendations(
            weak_points, category_mastery
        )
        
        return DiagnosticReport(
            learner_id=learner_id,
            weak_points=weak_points,
            overall_mastery=overall_mastery,
            recommendations=recommendations,
            error_summary=error_summary,
            category_mastery=category_mastery,
        )

    async def _calculate_category_mastery(
        self,
        learner_state: Dict[str, float],
    ) -> Dict[str, float]:
        """计算各类别的平均掌握度"""
        category_values: Dict[str, List[float]] = {}
        
        for kp_id, mastery in learner_state.items():
            kp = await self.kg.get_knowledge_point_by_id(kp_id)
            if kp:
                category = kp.get("category", "unknown")
                if category not in category_values:
                    category_values[category] = []
                category_values[category].append(mastery)
        
        return {
            cat: sum(values) / len(values)
            for cat, values in category_values.items()
            if values
        }

    async def _generate_recommendations(
        self,
        weak_points: List[WeakPoint],
        category_mastery: Dict[str, float],
    ) -> List[str]:
        """生成个性化建议"""
        recommendations = []
        
        # 基于薄弱点的建议
        if weak_points:
            root_causes = [wp for wp in weak_points if wp.root_cause]
            if root_causes:
                recommendations.append(
                    f"优先学习根本原因知识点: {root_causes[0].name}"
                )
        
        # 基于类别的建议
        for category, mastery in category_mastery.items():
            if mastery < 0.4:
                recommendations.append(f"加强{category}类知识的学习")
            elif mastery >= 0.7:
                recommendations.append(f"{category}掌握良好，可以挑战更高难度")
        
        # 通用建议
        if not recommendations:
            recommendations.append("继续保持学习，定期复习巩固")
        
        return recommendations
