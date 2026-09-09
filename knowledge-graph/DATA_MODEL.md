# Neo4j 知识图谱数据模型

## 节点类型

### 1. KnowledgePoint (知识点)
核心节点，表示法语知识体系中的一个知识点。

```cypher
(:KnowledgePoint {
    id: String,           // 唯一标识符，如 "grammar_prt_now"
    name: String,         // 名称，如 "直陈式现在时"
    level: String,        // CEFR等级: A1/A2/B1/B2
    category: String,     // 分类: vocabulary/grammar/verb_conjugation/accord
    subcategory: String,  // 子分类
    description: String,  // 详细描述
    difficulty: Float,    // 难度系数 0-1
    created_at: DateTime  // 创建时间
})
```

### 2. Exercise (练习题)
练习题节点，链接到考察的知识点。

```cypher
(:Exercise {
    id: String,           // 唯一标识符
    type: String,         // 题型: vocabulary/grammar/translation/reading/listening
    difficulty: Float,    // 难度系数 (IRT a参数)
    b_parameter: Float,   // IRT b参数
    c_parameter: Float,   // IRT c参数
    content: String,      // 题目内容
    options: List<String>, // 选项（选择题）
    correct_answer: String, // 正确答案
    explanation: String,  // 解析
    cognitive_level: String, // 布鲁姆认知层级
    estimated_time_ms: Int   // 预期答题时间(毫秒)
})
```

### 3. Lesson (课程)
课程节点，包含多个知识点。

```cypher
(:Lesson {
    id: String,           // 唯一标识符
    title: String,        // 课程标题
    level: String,        // CEFR等级
    order: Int,           // 课程顺序
    module: String        // 模块: vocabulary/grammar/reading/listening
})
```

### 4. Topic (主题)
词汇主题节点。

```cypher
(:Topic {
    id: String,           // 唯一标识符
    name: String,         // 主题名称
    level: String         // CEFR等级
})
```

## 关系类型

### 1. PREREQUISITE_OF (前置知识)
表示知识点之间的前置依赖关系。

```cypher
(:KnowledgePoint)-[:PREREQUISITE_OF {
    weight: Float,        // 依赖强度 0-1
    mandatory: Boolean    // 是否必须掌握
}]->(:KnowledgePoint)
```

### 2. BELONGS_TO (属于)
知识点属于某课程。

```cypher
(:KnowledgePoint)-[:BELONGS_TO]->(:Lesson)
```

### 3. TESTS (考察)
练习题考察某知识点。

```cypher
(:Exercise)-[:TESTS {
    weight: Float         // 考察权重
}]->(:KnowledgePoint)
```

### 4. RELATED_TO (相关)
知识点之间的相关关系。

```cypher
(:KnowledgePoint)-[:RELATED_TO {
    type: String          // 相关类型: similar/contrast/applied
}]->(:KnowledgePoint)
```

### 5. HAS_VOCABULARY (包含词汇)
主题包含词汇知识点。

```cypher
(:Topic)-[:HAS_VOCABULARY]->(:KnowledgePoint)
```

## 索引和约束

```cypher
-- 创建唯一性约束
CREATE CONSTRAINT kp_id_unique IF NOT EXISTS 
FOR (kp:KnowledgePoint) REQUIRE kp.id IS UNIQUE;

CREATE CONSTRAINT exercise_id_unique IF NOT EXISTS 
FOR (e:Exercise) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT lesson_id_unique IF NOT EXISTS 
FOR (l:Lesson) REQUIRE l.id IS UNIQUE;

CREATE CONSTRAINT topic_id_unique IF NOT EXISTS 
FOR (t:Topic) REQUIRE t.id IS UNIQUE;

-- 创建索引
CREATE INDEX kp_level_idx IF NOT EXISTS 
FOR (kp:KnowledgePoint) ON (kp.level);

CREATE INDEX kp_category_idx IF NOT EXISTS 
FOR (kp:KnowledgePoint) ON (kp.category);

CREATE INDEX exercise_type_idx IF NOT EXISTS 
FOR (e:Exercise) ON (e.type);
```

## 示例查询

```cypher
-- 1. 获取某知识点的所有前置知识
MATCH (prereq)-[:PREREQUISITE_OF]->(target {id: 'grammar_prt_compose'})
RETURN prereq.id, prereq.name, prereq.level
ORDER BY prereq.level;

-- 2. 查找从当前状态到目标知识点的学习路径
MATCH path = shortestPath(
    (start {id: 'grammar_prt_now'})-[:PREREQUISITE_OF*]->(end {id: 'grammar_subjonctif'})
)
RETURN [n IN nodes(path) | n.id] AS path;

-- 3. 获取某级别的所有知识点
MATCH (kp:KnowledgePoint {level: 'A1'})
RETURN kp.id, kp.name, kp.category
ORDER BY kp.category, kp.name;

-- 4. 获取某知识点的所有相关练习
MATCH (e:Exercise)-[:TESTS]->(kp {id: 'grammar_prt_now'})
RETURN e.id, e.type, e.difficulty, e.content
LIMIT 10;

-- 5. 分析学习者的薄弱点（需要结合学习者状态数据）
MATCH (kp:KnowledgePoint)
WHERE NOT EXISTS {
    MATCH (prereq)-[:PREREQUISITE_OF]->(kp)
    WHERE prereq.mastery < 0.6
}
RETURN kp.id, kp.name, kp.level;
```
