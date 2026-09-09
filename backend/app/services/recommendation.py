"""
推荐引擎模块
融合知识图谱路径推荐、协同过滤等多种策略
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from .knowledge_graph import KnowledgeGraphService
from .bkt import BKTService


@dataclass
class Recommendation:
    """推荐项"""
    knowledge_point_id: str
    name: str
    level: str
    category: str
    reason: str
    score: float
    prerequisites_met: bool = True


class RecommendationEngine:
    """推荐引擎"""

    def __init__(
        self,
        kg_service: KnowledgeGraphService,
        bkt_service: BKTService,
    ):
        self.kg = kg_service
        self.bkt = bkt_service

    async def get_recommendations(
        self,
        learner_state: Dict[str, float],
        target_level: str = "B1",
        n_recommendations: int = 5,
    ) -> List[Recommendation]:
        """
        生成个性化推荐
        
        Args:
            learner_state: 学习者知识状态 {skill_id: mastery}
            target_level: 目标等级
            n_recommendations: 推荐数量
            
        Returns:
            推荐列表
        """
        recommendations = []
        
        # 策略1: 知识图谱路径推荐
        kg_recs = await self._kg_path_recommend(learner_state, target_level)
        recommendations.extend(kg_recs)
        
        # 策略2: 基于薄弱点的推荐
        weak_recs = await self._weak_point_recommend(learner_state)
        recommendations.extend(weak_recs)
        
        # 策略3: 遗忘曲线复习推荐
        review_recs = await self._review_recommend(learner_state)
        recommendations.extend(review_recs)
        
        # 去重并排序
        seen_ids = set()
        unique_recs = []
        for rec in recommendations:
            if rec.knowledge_point_id not in seen_ids:
                seen_ids.add(rec.knowledge_point_id)
                unique_recs.append(rec)
        
        # 按分数排序
        unique_recs.sort(key=lambda x: x.score, reverse=True)
        
        return unique_recs[:n_recommendations]

    async def _kg_path_recommend(
        self,
        learner_state: Dict[str, float],
        target_level: str,
    ) -> List[Recommendation]:
        """基于知识图谱路径的推荐"""
        recommendations = []
        
        # 获取目标级别的知识点
        all_kps = await self.kg.get_all_knowledge_points(level=target_level)
        
        for kp in all_kps:
            kp_id = kp["id"]
            
            # 跳过已掌握的知识点
            if learner_state.get(kp_id, 0) >= 0.8:
                continue
            
            # 检查前置知识是否满足
            prereqs = await self.kg.get_prerequisites(kp_id)
            prereqs_met = True
            unmet_prereqs = []
            
            for prereq in prereqs:
                prereq_id = prereq["knowledge_point"]["id"]
                prereq_mastery = learner_state.get(prereq_id, 0)
                
                if prereq["mandatory"] and prereq_mastery < 0.6:
                    prereqs_met = False
                    unmet_prereqs.append(prereq_id)
            
            # 计算推荐分数
            current_mastery = learner_state.get(kp_id, 0)
            score = self._calculate_recommendation_score(
                current_mastery=current_mastery,
                difficulty=kp.get("difficulty", 0.5),
                prereqs_met=prereqs_met,
            )
            
            if prereqs_met:
                reason = f"适合当前水平，掌握度 {current_mastery:.0%}"
            else:
                reason = f"需要先掌握: {', '.join(unmet_prereqs[:2])}"
            
            recommendations.append(Recommendation(
                knowledge_point_id=kp_id,
                name=kp["name"],
                level=kp["level"],
                category=kp["category"],
                reason=reason,
                score=score,
                prerequisites_met=prereqs_met,
            ))
        
        return recommendations

    async def _weak_point_recommend(
        self,
        learner_state: Dict[str, float],
    ) -> List[Recommendation]:
        """基于薄弱点的推荐"""
        recommendations = []
        
        # 找出掌握度较低的知识点
        weak_points = [
            (kp_id, mastery) 
            for kp_id, mastery in learner_state.items()
            if mastery < 0.5
        ]
        
        # 按掌握度排序（最弱的优先）
        weak_points.sort(key=lambda x: x[1])
        
        for kp_id, mastery in weak_points[:5]:
            kp = await self.kg.get_knowledge_point_by_id(kp_id)
            if kp:
                score = 1.0 - mastery  # 越弱分数越高
                reason = f"薄弱知识点，掌握度仅 {mastery:.0%}"
                
                recommendations.append(Recommendation(
                    knowledge_point_id=kp_id,
                    name=kp["name"],
                    level=kp["level"],
                    category=kp["category"],
                    reason=reason,
                    score=score,
                    prerequisites_met=True,
                ))
        
        return recommendations

    async def _review_recommend(
        self,
        learner_state: Dict[str, float],
    ) -> List[Recommendation]:
        """基于遗忘曲线的复习推荐"""
        recommendations = []
        
        # 找出需要复习的知识点（掌握度在中等水平）
        review_candidates = [
            (kp_id, mastery)
            for kp_id, mastery in learner_state.items()
            if 0.5 <= mastery < 0.8
        ]
        
        for kp_id, mastery in review_candidates[:3]:
            kp = await self.kg.get_knowledge_point_by_id(kp_id)
            if kp:
                # 需要复习的紧迫度
                score = 0.7 + (0.8 - mastery)
                reason = f"建议复习，巩固掌握度 {mastery:.0%}"
                
                recommendations.append(Recommendation(
                    knowledge_point_id=kp_id,
                    name=kp["name"],
                    level=kp["level"],
                    category=kp["category"],
                    reason=reason,
                    score=score,
                    prerequisites_met=True,
                ))
        
        return recommendations

    def _calculate_recommendation_score(
        self,
        current_mastery: float,
        difficulty: float,
        prereqs_met: bool,
    ) -> float:
        """
        计算推荐分数
        
        分数越高越推荐
        """
        # 基础分数：掌握度越低，越需要学习
        base_score = 1.0 - current_mastery
        
        # 难度调整：中等难度最合适
        difficulty_factor = 1.0 - abs(difficulty - 0.5)
        
        # 前置知识满足度调整
        prereq_factor = 1.0 if prereqs_met else 0.3
        
        # 综合分数
        score = base_score * 0.5 + difficulty_factor * 0.3 + prereq_factor * 0.2
        
        return min(max(score, 0.0), 1.0)

    async def get_learning_path_recommendation(
        self,
        learner_state: Dict[str, float],
        target_kp_id: str,
    ) -> List[Recommendation]:
        """
        获取学习路径推荐
        
        Args:
            learner_state: 学习者知识状态
            target_kp_id: 目标知识点ID
            
        Returns:
            按顺序排列的学习路径推荐
        """
        recommendations = []
        
        # 获取完整前置链
        chain = await self.kg.get_prerequisite_chain(target_kp_id)
        
        # 过滤掉已掌握的
        unmastered = [
            item for item in chain
            if learner_state.get(item["knowledge_point"]["id"], 0) < 0.8
        ]
        
        # 按距离排序（先学基础）
        unmastered.sort(key=lambda x: x["distance"])
        
        for item in unmastered:
            kp = item["knowledge_point"]
            kp_id = kp["id"]
            mastery = learner_state.get(kp_id, 0)
            
            reason = f"路径步骤 (距离目标 {item['distance']} 步)"
            score = 1.0 - mastery
            
            recommendations.append(Recommendation(
                knowledge_point_id=kp_id,
                name=kp["name"],
                level=kp["level"],
                category=kp["category"],
                reason=reason,
                score=score,
                prerequisites_met=True,
            ))
        
        return recommendations
