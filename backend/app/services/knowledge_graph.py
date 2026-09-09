"""
知识图谱服务模块
提供知识图谱查询、路径规划等功能
"""

from typing import List, Dict, Optional
from neo4j import AsyncDriver, AsyncSession


class KnowledgeGraphService:
    """知识图谱服务"""

    def __init__(self, driver: AsyncDriver):
        self.driver = driver

    async def get_all_knowledge_points(
        self, 
        level: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict]:
        """获取所有知识点"""
        query = "MATCH (kp:KnowledgePoint)"
        params = {}
        conditions = []
        
        if level:
            conditions.append("kp.level = $level")
            params["level"] = level
        if category:
            conditions.append("kp.category = $category")
            params["category"] = category
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " RETURN kp ORDER BY kp.level, kp.category, kp.name"
        
        async with self.driver.session() as session:
            result = await session.run(query, **params)
            records = await result.data()
            return [record["kp"] for record in records]

    async def get_knowledge_point_by_id(self, kp_id: str) -> Optional[Dict]:
        """根据ID获取知识点"""
        query = """
        MATCH (kp:KnowledgePoint {id: $id})
        RETURN kp
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=kp_id)
            record = await result.single()
            return record["kp"] if record else None

    async def get_prerequisites(self, kp_id: str) -> List[Dict]:
        """获取某知识点的前置知识"""
        query = """
        MATCH (prereq:KnowledgePoint)-[:PREREQUISITE_OF]->(target:KnowledgePoint {id: $id})
        RETURN prereq, r.weight AS weight, r.mandatory AS mandatory
        ORDER BY prereq.level
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=kp_id)
            records = await result.data()
            return [
                {
                    "knowledge_point": record["prereq"],
                    "weight": record["weight"],
                    "mandatory": record["mandatory"],
                }
                for record in records
            ]

    async def get_prerequisite_chain(self, kp_id: str, max_depth: int = 5) -> List[Dict]:
        """获取知识点的完整前置依赖链"""
        query = """
        MATCH path = (prereq:KnowledgePoint)-[:PREREQUISITE_OF*1..$max_depth]->(target:KnowledgePoint {id: $id})
        RETURN DISTINCT prereq, length(path) AS distance
        ORDER BY distance
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=kp_id, max_depth=max_depth)
            records = await result.data()
            return [
                {
                    "knowledge_point": record["prereq"],
                    "distance": record["distance"],
                }
                for record in records
            ]

    async def get_dependents(self, kp_id: str) -> List[Dict]:
        """获取依赖某知识点的后续知识点"""
        query = """
        MATCH (source:KnowledgePoint {id: $id})-[:PREREQUISITE_OF]->(dependent:KnowledgePoint)
        RETURN dependent, r.weight AS weight
        """
        async with self.driver.session() as session:
            result = await session.run(query, id=kp_id)
            records = await result.data()
            return [
                {
                    "knowledge_point": record["dependent"],
                    "weight": record["weight"],
                }
                for record in records
            ]

    async def find_learning_path(
        self, 
        current_kp_id: str, 
        target_kp_id: str
    ) -> List[str]:
        """查找从当前知识点到目标知识点的学习路径"""
        query = """
        MATCH path = shortestPath(
            (start:KnowledgePoint {id: $current})-[:PREREQUISITE_OF*]->(end:KnowledgePoint {id: $target})
        )
        RETURN [n IN nodes(path) | n.id] AS path
        """
        async with self.driver.session() as session:
            result = await session.run(
                query, current=current_kp_id, target=target_kp_id
            )
            record = await result.single()
            return record["path"] if record else []

    async def find_all_paths(
        self, 
        current_kp_id: str, 
        target_kp_id: str,
        max_length: int = 10
    ) -> List[List[str]]:
        """查找所有可能的学习路径"""
        query = """
        MATCH path = (start:KnowledgePoint {id: $current})-[:PREREQUISITE_OF*1..$max_length]->(end:KnowledgePoint {id: $target})
        RETURN [n IN nodes(path) | n.id] AS path, length(path) AS length
        ORDER BY length
        LIMIT 5
        """
        async with self.driver.session() as session:
            result = await session.run(
                query, current=current_kp_id, target=target_kp_id, max_length=max_length
            )
            records = await result.data()
            return [record["path"] for record in records]

    async def get_knowledge_graph_for_visualization(
        self,
        level: Optional[str] = None,
        max_nodes: int = 100
    ) -> Dict:
        """获取用于可视化知识图谱数据"""
        query = "MATCH (kp:KnowledgePoint)"
        params = {}
        
        if level:
            query += " WHERE kp.level = $level"
            params["level"] = level
        
        query += f" RETURN kp LIMIT {max_nodes}"
        
        async with self.driver.session() as session:
            result = await session.run(query, **params)
            kp_records = await result.data()
            nodes = [record["kp"] for record in kp_records]
            
            # 获取节点之间的关系
            node_ids = [node["id"] for node in nodes]
            if node_ids:
                rel_query = """
                MATCH (source:KnowledgePoint)-[r:PREREQUISITE_OF]->(target:KnowledgePoint)
                WHERE source.id IN $node_ids AND target.id IN $node_ids
                RETURN source.id AS source, target.id AS target, type(r) AS type, r.weight AS weight
                """
                result = await session.run(rel_query, node_ids=node_ids)
                rel_records = await result.data()
                edges = [
                    {
                        "source": record["source"],
                        "target": record["target"],
                        "type": record["type"],
                        "weight": record["weight"],
                    }
                    for record in rel_records
                ]
            else:
                edges = []
            
            return {"nodes": nodes, "edges": edges}

    async def get_statistics(self) -> Dict:
        """获取知识图谱统计信息"""
        async with self.driver.session() as session:
            # 节点统计
            result = await session.run(
                "MATCH (kp:KnowledgePoint) RETURN count(kp) AS count"
            )
            kp_count = (await result.single())["count"]
            
            result = await session.run(
                "MATCH (t:Topic) RETURN count(t) AS count"
            )
            topic_count = (await result.single())["count"]
            
            # 关系统计
            result = await session.run(
                "MATCH ()-[r:PREREQUISITE_OF]->() RETURN count(r) AS count"
            )
            prereq_count = (await result.single())["count"]
            
            # 级别分布
            result = await session.run(
                "MATCH (kp:KnowledgePoint) RETURN kp.level AS level, count(kp) AS count ORDER BY level"
            )
            level_dist = {record["level"]: record["count"] for record in await result.data()}
            
            # 类别分布
            result = await session.run(
                "MATCH (kp:KnowledgePoint) RETURN kp.category AS category, count(kp) AS count ORDER BY category"
            )
            category_dist = {record["category"]: record["count"] for record in await result.data()}
            
            return {
                "knowledge_points": kp_count,
                "topics": topic_count,
                "prerequisite_relationships": prereq_count,
                "level_distribution": level_dist,
                "category_distribution": category_dist,
            }
