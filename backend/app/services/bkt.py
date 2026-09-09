"""
贝叶斯知识追踪（BKT）服务模块
实现学习者知识状态的追踪和预测
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
import math


@dataclass
class BKTParameters:
    """BKT模型参数"""
    p_L0: float = 0.3      # 初始掌握概率
    p_T: float = 0.1       # 学习转移概率
    p_S: float = 0.1       # 失误概率（slip）
    p_G: float = 0.25      # 猜测概率（guess）


class BKTService:
    """贝叶斯知识追踪服务"""

    def __init__(self, params: Optional[BKTParameters] = None):
        self.params = params or BKTParameters()
        # 可以为不同知识点配置不同的参数
        self.skill_params: Dict[str, BKTParameters] = {}

    def get_params(self, skill_id: str) -> BKTParameters:
        """获取特定技能的BKT参数"""
        return self.skill_params.get(skill_id, self.params)

    def set_params(self, skill_id: str, params: BKTParameters):
        """设置特定技能的BKT参数"""
        self.skill_params[skill_id] = params

    def initialize_mastery(self, skill_id: str) -> float:
        """初始化学习者对某技能的掌握概率"""
        params = self.get_params(skill_id)
        return params.p_L0

    def update_mastery(
        self, 
        current_mastery: float, 
        correct: bool, 
        skill_id: str = "default"
    ) -> float:
        """
        根据答题结果更新掌握概率
        
        Args:
            current_mastery: 当前掌握概率 P(L)
            correct: 是否答对
            skill_id: 技能ID
            
        Returns:
            更新后的掌握概率
        """
        params = self.get_params(skill_id)
        
        p_L_new: float
        if correct:
            # P(L|correct) = P(correct|L) * P(L) / P(correct)
            p_correct = current_mastery * (1 - params.p_S) + (1 - current_mastery) * params.p_G
            p_L_given_correct = current_mastery * (1 - params.p_S) / p_correct
            # 应用学习转移
            p_L_new = p_L_given_correct + (1 - p_L_given_correct) * params.p_T
        else:
            # P(L|incorrect) = P(incorrect|L) * P(L) / P(incorrect)
            p_incorrect = current_mastery * params.p_S + (1 - current_mastery) * (1 - params.p_G)
            p_L_given_incorrect = current_mastery * params.p_S / p_incorrect
            # 应用学习转移
            p_L_new = p_L_given_incorrect + (1 - p_L_given_incorrect) * params.p_T
        
        # 限制在合理范围内
        return min(max(p_L_new, 0.01), 0.99)

    def predict_correct_probability(
        self, 
        mastery: float, 
        skill_id: str = "default"
    ) -> float:
        """
        预测下次答对的概率
        
        Args:
            mastery: 当前掌握概率
            skill_id: 技能ID
            
        Returns:
            预测答对概率
        """
        params = self.get_params(skill_id)
        return mastery * (1 - params.p_S) + (1 - mastery) * params.p_G

    def batch_update(
        self,
        initial_mastery: float,
        responses: List[bool],
        skill_id: str = "default"
    ) -> List[float]:
        """
        批量更新掌握概率
        
        Args:
            initial_mastery: 初始掌握概率
            responses: 答题结果列表
            skill_id: 技能ID
            
        Returns:
            每次更新后的掌握概率列表
        """
        mastery_history = [initial_mastery]
        current_mastery = initial_mastery
        
        for correct in responses:
            current_mastery = self.update_mastery(current_mastery, correct, skill_id)
            mastery_history.append(current_mastery)
        
        return mastery_history

    def get_mastery_level(self, mastery: float) -> str:
        """
        根据掌握概率返回掌握水平描述
        
        Args:
            mastery: 掌握概率
            
        Returns:
            掌握水平描述
        """
        if mastery >= 0.9:
            return "精通"
        elif mastery >= 0.7:
            return "熟练"
        elif mastery >= 0.5:
            return "了解"
        elif mastery >= 0.3:
            return "初步"
        else:
            return "未掌握"

    def calculate_knowledge_state(
        self,
        skill_masteries: Dict[str, float]
    ) -> Dict:
        """
        计算综合知识状态
        
        Args:
            skill_masteries: 各技能掌握概率字典
            
        Returns:
            综合知识状态
        """
        if not skill_masteries:
            return {
                "overall_mastery": 0.0,
                "mastered_count": 0,
                "learning_count": 0,
                "weak_count": 0,
                "category_mastery": {},
            }
        
        values = list(skill_masteries.values())
        overall_mastery = sum(values) / len(values)
        
        mastered_count = sum(1 for v in values if v >= 0.8)
        learning_count = sum(1 for v in values if 0.3 <= v < 0.8)
        weak_count = sum(1 for v in values if v < 0.3)
        
        return {
            "overall_mastery": overall_mastery,
            "mastered_count": mastered_count,
            "learning_count": learning_count,
            "weak_count": weak_count,
            "skill_count": len(skill_masteries),
        }

    def suggest_review(
        self,
        skill_masteries: Dict[str, float],
        days_since_practiced: Dict[str, int],
        forgetting_rate: float = 0.1
    ) -> List[Dict]:
        """
        建议需要复习的知识点
        
        Args:
            skill_masteries: 各技能掌握概率
            days_since_practiced: 各技能距上次练习天数
            forgetting_rate: 遗忘速率
            
        Returns:
            需要复习的知识点列表
        """
        suggestions = []
        
        for skill_id, mastery in skill_masteries.items():
            days = days_since_practiced.get(skill_id, 0)
            
            # 模拟遗忘
            estimated_mastery = mastery * math.exp(-forgetting_rate * days)
            
            if estimated_mastery < 0.6:
                suggestions.append({
                    "skill_id": skill_id,
                    "current_mastery": mastery,
                    "estimated_mastery": estimated_mastery,
                    "days_since_practiced": days,
                    "urgency": "high" if estimated_mastery < 0.3 else "medium",
                })
        
        # 按紧急程度排序
        suggestions.sort(key=lambda x: x["estimated_mastery"])
        
        return suggestions
