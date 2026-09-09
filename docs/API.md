# API文档

## 目录

- [概述](#概述)
- [认证](#认证)
- [健康检查API](#健康检查api)
- [学习者API](#学习者api)
- [知识图谱API](#知识图谱api)
- [练习API](#练习api)
- [诊断API](#诊断api)
- [错误处理](#错误处理)

---

## 概述

### 基础信息

- **Base URL**: `http://localhost:8000/api`
- **协议**: HTTP/HTTPS
- **数据格式**: JSON
- **字符编码**: UTF-8

### 交互式文档

启动后端服务后，访问以下地址查看交互式API文档：
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

---

## 认证

当前版本暂未实现认证机制。后续版本将支持JWT Token认证。

---

## 健康检查API

### GET /api/health

检查API服务是否正常运行。

**响应示例：**

```json
{
  "status": "healthy",
  "service": "iFrench Learning API"
}
```

### GET /api/health/neo4j

检查Neo4j数据库连接状态。

**响应示例：**

```json
{
  "status": "healthy",
  "database": "neo4j",
  "result": 1
}
```

### GET /api/health/postgres

检查PostgreSQL数据库连接状态。

**响应示例：**

```json
{
  "status": "healthy",
  "database": "postgres",
  "result": 1
}
```

---

## 学习者API

### GET /api/learners

获取学习者列表。

**参数：**

| 参数 | 类型 | 默认值 | 说明 |
|:--|:--|:--|:--|
| skip | int | 0 | 跳过数量 |
| limit | int | 100 | 返回数量 |

**响应示例：**

```json
[
  {
    "id": "uuid-1234",
    "name": "张三",
    "level": "A1",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### POST /api/learners

创建新学习者。

**请求体：**

```json
{
  "name": "张三",
  "level": "A1"
}
```

**响应示例：**

```json
{
  "id": "uuid-1234",
  "name": "张三",
  "level": "A1",
  "created_at": "2024-01-01T00:00:00"
}
```

### GET /api/learners/{learner_id}/state

获取学习者知识状态。

**路径参数：**

| 参数 | 类型 | 说明 |
|:--|:--|:--|
| learner_id | string | 学习者ID |

**响应示例：**

```json
{
  "learner_id": "uuid-1234",
  "knowledge_state": {
    "grammar_noun_gender": 0.85,
    "grammar_article_def": 0.72,
    "vocab_bonjour": 0.95
  },
  "overall_mastery": 0.84,
  "last_updated": "2024-01-01T12:00:00"
}
```

---

## 知识图谱API

### GET /api/knowledge-graph

获取知识图谱数据。

**查询参数：**

| 参数 | 类型 | 默认值 | 说明 |
|:--|:--|:--|:--|
| level | string | null | CEFR等级筛选 (A1/A2/B1/B2) |
| max_nodes | int | 100 | 最大节点数 |

**响应示例：**

```json
{
  "nodes": [
    {
      "id": "grammar_prt_now",
      "name": "直陈式现在时",
      "level": "A1",
      "category": "verb_conjugation",
      "difficulty": 0.35
    }
  ],
  "edges": [
    {
      "source": "grammar_noun_gender",
      "target": "grammar_prt_now",
      "type": "PREREQUISITE_OF",
      "weight": 0.5
    }
  ]
}
```

### GET /api/knowledge-graph/stats

获取知识图谱统计信息。

**响应示例：**

```json
{
  "knowledge_points": 70,
  "topics": 16,
  "prerequisite_relationships": 28,
  "level_distribution": {
    "A1": 35,
    "A2": 25,
    "B1": 10
  },
  "category_distribution": {
    "grammar": 30,
    "vocabulary": 40,
    "verb_conjugation": 15,
    "accord": 5
  }
}
```

### GET /api/knowledge-graph/{node_id}

获取知识点详情。

**路径参数：**

| 参数 | 类型 | 说明 |
|:--|:--|:--|
| node_id | string | 知识点ID |

**响应示例：**

```json
{
  "id": "grammar_prt_now",
  "name": "直陈式现在时",
  "level": "A1",
  "category": "verb_conjugation",
  "subcategory": "indicatif_present",
  "description": "法语动词现在时变位规则",
  "difficulty": 0.35
}
```

### GET /api/knowledge-graph/{node_id}/prerequisites

获取知识点的前置知识。

**响应示例：**

```json
{
  "node_id": "grammar_prt_passe_compose",
  "prerequisites": [
    {
      "knowledge_point": {
        "id": "grammar_prt_now",
        "name": "直陈式现在时"
      },
      "weight": 0.8,
      "mandatory": true
    }
  ]
}
```

### GET /api/knowledge-graph/{node_id}/dependents

获取依赖此知识点的后续知识点。

**响应示例：**

```json
{
  "node_id": "grammar_prt_now",
  "dependents": [
    {
      "knowledge_point": {
        "id": "grammar_prt_passe_compose",
        "name": "复合过去时"
      },
      "weight": 0.8
    }
  ]
}
```

### GET /api/knowledge-graph/path/{current}/{target}

查找学习路径。

**路径参数：**

| 参数 | 类型 | 说明 |
|:--|:--|:--|
| current | string | 当前知识点ID |
| target | string | 目标知识点ID |

**响应示例：**

```json
{
  "current": "grammar_prt_now",
  "target": "grammar_subjonctif",
  "path": [
    "grammar_prt_now",
    "grammar_prt_imparfait",
    "grammar_subjonctif"
  ]
}
```

---

## 练习API

### POST /api/exercises/recommend

获取推荐练习。

**请求体：**

```json
{
  "learner_id": "uuid-1234",
  "knowledge_state": {
    "grammar_prt_now": 0.85,
    "grammar_article_def": 0.72
  },
  "target_level": "A1",
  "n_recommendations": 5
}
```

**响应示例：**

```json
{
  "learner_id": "uuid-1234",
  "recommendations": [
    {
      "knowledge_point_id": "grammar_prt_passe_compose",
      "name": "复合过去时",
      "level": "A1",
      "category": "verb_conjugation",
      "reason": "适合当前水平，掌握度 35%",
      "score": 0.75
    }
  ]
}
```

### POST /api/exercises/submit

提交练习答案。

**请求体：**

```json
{
  "learner_id": "uuid-1234",
  "exercise_id": "ex-001",
  "knowledge_point_id": "grammar_article_def",
  "correct": true,
  "response_time_ms": 5000
}
```

**响应示例：**

```json
{
  "exercise_id": "ex-001",
  "correct": true,
  "new_mastery": 0.78,
  "mastery_level": "熟练"
}
```

### POST /api/exercises/learning-path

获取学习路径推荐。

**请求体：**

```json
{
  "knowledge_state": {
    "grammar_prt_now": 0.85
  },
  "target_kp_id": "grammar_subjonctif"
}
```

**响应示例：**

```json
{
  "target": "grammar_subjonctif",
  "path": [
    {
      "knowledge_point_id": "grammar_prt_imparfait",
      "name": "未完成过去时",
      "reason": "路径步骤 (距离目标 1 步)"
    }
  ]
}
```

### POST /api/exercises/update-mastery

更新知识点掌握度。

**请求体：**

```json
{
  "skill_id": "grammar_article_def",
  "current_mastery": 0.72,
  "correct": true
}
```

**响应示例：**

```json
{
  "skill_id": "grammar_article_def",
  "previous_mastery": 0.72,
  "new_mastery": 0.78,
  "correct": true,
  "mastery_level": "熟练"
}
```

---

## 诊断API

### POST /api/diagnostics/analyze

分析学习者薄弱点。

**请求体：**

```json
{
  "learner_id": "uuid-1234",
  "knowledge_state": {
    "grammar_prt_now": 0.85,
    "grammar_prt_passe_compose": 0.25,
    "grammar_auxiliaire": 0.35
  },
  "error_history": [
    {
      "exercise_id": "ex-001",
      "category": "verb_conjugation",
      "error_type": "tense_error"
    }
  ]
}
```

**响应示例：**

```json
{
  "learner_id": "uuid-1234",
  "weak_points": [
    {
      "knowledge_point_id": "grammar_prt_passe_compose",
      "name": "复合过去时",
      "level": "A1",
      "category": "verb_conjugation",
      "mastery": 0.25,
      "confidence": 0.75,
      "root_cause": true
    }
  ],
  "overall_mastery": 0.48,
  "recommendations": [
    "优先学习根本原因知识点: 复合过去时",
    "加强 verb_conjugation 类知识的学习"
  ],
  "error_summary": {
    "verb_conjugation": 5
  },
  "category_mastery": {
    "grammar": 0.72,
    "verb_conjugation": 0.35
  }
}
```

### POST /api/diagnostics/root-cause

根因分析。

**查询参数：**

| 参数 | 类型 | 说明 |
|:--|:--|:--|
| error_kp_id | string | 出错的知识点ID |
| knowledge_state | object | 学习者知识状态 |

**响应示例：**

```json
{
  "root_causes": [
    {
      "knowledge_point_id": "grammar_auxiliaire",
      "name": "助动词 avoir/être",
      "mastery": 0.35,
      "confidence": 0.65,
      "depth": 1
    }
  ]
}
```

---

## 错误处理

### HTTP状态码

| 状态码 | 说明 |
|:--|:--|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 错误响应格式

```json
{
  "detail": "Error message"
}
```

### 示例错误响应

```json
{
  "detail": "Knowledge point not found"
}
```

---

## 数据模型

### KnowledgePoint

```json
{
  "id": "string",
  "name": "string",
  "level": "A1|A2|B1|B2",
  "category": "grammar|vocabulary|verb_conjugation|accord",
  "subcategory": "string",
  "description": "string",
  "difficulty": 0.0-1.0
}
```

### Learner

```json
{
  "id": "string (UUID)",
  "name": "string",
  "level": "A1|A2|B1|B2",
  "created_at": "datetime"
}
```

### Recommendation

```json
{
  "knowledge_point_id": "string",
  "name": "string",
  "level": "string",
  "category": "string",
  "reason": "string",
  "score": 0.0-1.0
}
```

### WeakPoint

```json
{
  "knowledge_point_id": "string",
  "name": "string",
  "level": "string",
  "category": "string",
  "mastery": 0.0-1.0,
  "confidence": 0.0-1.0,
  "root_cause": "boolean"
}
```
