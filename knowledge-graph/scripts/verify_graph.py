#!/usr/bin/env python3
"""
Neo4j知识图谱验证脚本
用于验证导入的知识图谱数据完整性
"""

import os
from neo4j import GraphDatabase

# 配置
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "ifrench_neo4j_2024")


def verify_counts(session):
    """验证节点和关系数量"""
    print("\n=== 节点统计 ===")
    result = session.run("MATCH (n) RETURN labels(n) AS label, count(n) AS count")
    for record in result:
        print(f"  {record['label']}: {record['count']}")
    
    print("\n=== 关系统计 ===")
    result = session.run("MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count")
    for record in result:
        print(f"  {record['type']}: {record['count']}")


def verify_prerequisites(session):
    """验证前置关系完整性"""
    print("\n=== 前置关系验证 ===")
    
    # 检查是否有悬空的前置关系
    result = session.run("""
        MATCH (source)-[r:PREREQUISITE_OF]->(target)
        WHERE NOT EXISTS {
            MATCH (kp:KnowledgePoint {id: source.id})
        } OR NOT EXISTS {
            MATCH (kp:KnowledgePoint {id: target.id})
        }
        RETURN source.id, target.id
    """)
    dangling = list(result)
    if dangling:
        print(f"  WARNING: Found {len(dangling)} dangling prerequisite relationships")
        for record in dangling:
            print(f"    {record[0]} -> {record[1]}")
    else:
        print("  OK: No dangling prerequisite relationships")


def verify_knowledge_levels(session):
    """验证知识点级别分布"""
    print("\n=== 知识点级别分布 ===")
    result = session.run("""
        MATCH (kp:KnowledgePoint)
        RETURN kp.level AS level, count(kp) AS count
        ORDER BY level
    """)
    for record in result:
        print(f"  Level {record['level']}: {record['count']} knowledge points")


def verify_categories(session):
    """验证知识点类别分布"""
    print("\n=== 知识点类别分布 ===")
    result = session.run("""
        MATCH (kp:KnowledgePoint)
        RETURN kp.category AS category, count(kp) AS count
        ORDER BY category
    """)
    for record in result:
        print(f"  {record['category']}: {record['count']}")


def verify_topics(session):
    """验证主题-词汇关系"""
    print("\n=== 主题-词汇关系 ===")
    result = session.run("""
        MATCH (t:Topic)-[:HAS_VOCABULARY]->(kp:KnowledgePoint)
        RETURN t.name AS topic, count(kp) AS vocab_count
        ORDER BY vocab_count DESC
    """)
    for record in result:
        print(f"  {record['topic']}: {record['vocab_count']} words")


def verify_learning_paths(session):
    """验证学习路径示例"""
    print("\n=== 学习路径示例 ===")
    
    # 示例：从基础语法到虚拟式
    result = session.run("""
        MATCH path = shortestPath(
            (start {id: 'grammar_prt_now'})-[:PREREQUISITE_OF*]->(end {id: 'grammar_subjonctif'})
        )
        RETURN [n IN nodes(path) | n.name] AS path, length(path) AS length
    """)
    for record in result:
        print(f"  直陈式现在时 -> 虚拟式:")
        print(f"    路径: {' -> '.join(record['path'])}")
        print(f"    步数: {record['length']}")


def main():
    """主函数"""
    print(f"Connecting to Neo4j at {NEO4J_URI}...")
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            verify_counts(session)
            verify_prerequisites(session)
            verify_knowledge_levels(session)
            verify_categories(session)
            verify_topics(session)
            verify_learning_paths(session)
            
            print("\n=== 验证完成 ===")
            
    finally:
        driver.close()


if __name__ == "__main__":
    main()
