#!/usr/bin/env python3
"""
Neo4j知识图谱数据导入脚本
用于将JSON数据导入到Neo4j图数据库
"""

import json
import os
from pathlib import Path
from neo4j import GraphDatabase

# 配置
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "ifrench_neo4j_2024")

# 数据目录
DATA_DIR = Path(__file__).parent.parent / "data"


def create_constraints(session):
    """创建索引和约束"""
    constraints = [
        "CREATE CONSTRAINT kp_id_unique IF NOT EXISTS FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE",
        "CREATE CONSTRAINT exercise_id_unique IF NOT EXISTS FOR (e:Exercise) REQUIRE e.id IS UNIQUE",
        "CREATE CONSTRAINT lesson_id_unique IF NOT EXISTS FOR (l:Lesson) REQUIRE l.id IS UNIQUE",
        "CREATE CONSTRAINT topic_id_unique IF NOT EXISTS FOR (t:Topic) REQUIRE t.id IS UNIQUE",
        "CREATE INDEX kp_level_idx IF NOT EXISTS FOR (kp:KnowledgePoint) ON (kp.level)",
        "CREATE INDEX kp_category_idx IF NOT EXISTS FOR (kp:KnowledgePoint) ON (kp.category)",
        "CREATE INDEX exercise_type_idx IF NOT EXISTS FOR (e:Exercise) ON (e.type)",
    ]
    
    for constraint in constraints:
        session.run(constraint)
        print(f"Created constraint: {constraint[:50]}...")


def import_grammar(session, data):
    """导入语法知识数据"""
    # 导入知识点
    for kp in data["knowledge_points"]:
        session.run(
            """
            MERGE (kp:KnowledgePoint {id: $id})
            SET kp.name = $name,
                kp.level = $level,
                kp.category = $category,
                kp.subcategory = $subcategory,
                kp.description = $description,
                kp.difficulty = $difficulty,
                kp.created_at = datetime()
            """,
            id=kp["id"],
            name=kp["name"],
            level=kp["level"],
            category=kp["category"],
            subcategory=kp["subcategory"],
            description=kp["description"],
            difficulty=kp["difficulty"],
        )
    print(f"Imported {len(data['knowledge_points'])} grammar knowledge points")
    
    # 导入前置关系
    for prereq in data["prerequisites"]:
        session.run(
            """
            MATCH (source:KnowledgePoint {id: $source_id})
            MATCH (target:KnowledgePoint {id: $target_id})
            MERGE (source)-[r:PREREQUISITE_OF]->(target)
            SET r.weight = $weight,
                r.mandatory = $mandatory
            """,
            source_id=prereq["source"],
            target_id=prereq["target"],
            weight=prereq["weight"],
            mandatory=prereq["mandatory"],
        )
    print(f"Imported {len(data['prerequisites'])} prerequisite relationships")


def import_vocabulary(session, data):
    """导入词汇知识数据"""
    # 导入主题
    for topic in data["topics"]:
        session.run(
            """
            MERGE (t:Topic {id: $id})
            SET t.name = $name,
                t.level = $level,
                t.description = $description
            """,
            id=topic["id"],
            name=topic["name"],
            level=topic["level"],
            description=topic["description"],
        )
    print(f"Imported {len(data['topics'])} topics")
    
    # 导入词汇知识点
    for vocab in data["vocabulary"]:
        session.run(
            """
            MERGE (kp:KnowledgePoint {id: $id})
            SET kp.name = $name,
                kp.level = $level,
                kp.category = 'vocabulary',
                kp.subcategory = $topic,
                kp.description = $translation,
                kp.difficulty = $difficulty,
                kp.translation = $translation,
                kp.example = $example,
                kp.created_at = datetime()
            """,
            id=vocab["id"],
            name=vocab["name"],
            level=vocab["level"],
            topic=vocab["topic"],
            translation=vocab["translation"],
            difficulty=vocab["difficulty"],
            example=vocab["example"],
        )
    print(f"Imported {len(data['vocabulary'])} vocabulary knowledge points")
    
    # 导入主题-词汇关系
    for tv in data["topics_vocabulary"]:
        for vocab_id in tv["vocabulary"]:
            session.run(
                """
                MATCH (t:Topic {id: $topic_id})
                MATCH (kp:KnowledgePoint {id: $vocab_id})
                MERGE (t)-[:HAS_VOCABULARY]->(kp)
                """,
                topic_id=tv["topic"],
                vocab_id=vocab_id,
            )
    print(f"Imported topic-vocabulary relationships")
    
    # 导入词汇前置关系（词汇依赖语法知识）
    for vocab in data["vocabulary"]:
        for prereq_id in vocab.get("prerequisites", []):
            session.run(
                """
                MATCH (prereq:KnowledgePoint {id: $prereq_id})
                MATCH (target:KnowledgePoint {id: $target_id})
                MERGE (prereq)-[:PREREQUISITE_OF]->(target)
                SET r.weight = 0.5,
                    r.mandatory = false
                """,
                prereq_id=prereq_id,
                target_id=vocab["id"],
            )
    print(f"Imported vocabulary prerequisite relationships")


def clear_database(session):
    """清空数据库（谨慎使用）"""
    session.run("MATCH (n) DETACH DELETE n")
    print("Database cleared")


def main():
    """主函数"""
    print(f"Connecting to Neo4j at {NEO4J_URI}...")
    
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            # 创建约束
            print("\nCreating constraints...")
            create_constraints(session)
            
            # 清空数据库（可选，生产环境慎用）
            clear = input("\nClear database before import? (y/N): ").strip().lower()
            if clear == "y":
                clear_database(session)
            
            # 导入语法数据
            print("\nImporting grammar data...")
            grammar_file = DATA_DIR / "grammar.json"
            if grammar_file.exists():
                with open(grammar_file, "r", encoding="utf-8") as f:
                    grammar_data = json.load(f)
                import_grammar(session, grammar_data)
            
            # 导入词汇数据
            print("\nImporting vocabulary data...")
            vocab_file = DATA_DIR / "vocabulary.json"
            if vocab_file.exists():
                with open(vocab_file, "r", encoding="utf-8") as f:
                    vocab_data = json.load(f)
                import_vocabulary(session, vocab_data)
            
            # 验证导入
            print("\nVerifying import...")
            result = session.run("MATCH (n) RETURN labels(n) AS label, count(n) AS count")
            for record in result:
                print(f"  {record['label']}: {record['count']} nodes")
            
            result = session.run("MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count")
            for record in result:
                print(f"  {record['type']}: {record['count']} relationships")
            
            print("\nImport completed successfully!")
            
    finally:
        driver.close()


if __name__ == "__main__":
    main()
