# 法语自适应智能学习系统 - 实施计划

## 项目概述
基于知识图谱的法语自适应智能学习系统，覆盖CEFR A1-B2级别，包含词汇·语法·阅读·听力四个模块。

---

## 阶段1：项目初始化与基础设施
**目标**：搭建完整的开发环境和基础架构
**预计时间**：2-3天

### 1.1 创建项目目录结构
```
iFrenchLearning/
├── frontend/              # React前端
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── pages/         # 页面
│   │   ├── services/      # API服务
│   │   ├── stores/        # 状态管理
│   │   └── utils/         # 工具函数
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI后端
│   ├── app/
│   │   ├── api/           # 路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic模式
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   ├── requirements.txt
│   └── Dockerfile
├── knowledge-graph/       # 知识图谱数据与脚本
│   ├── data/              # JSON数据文件
│   └── scripts/           # 导入脚本
├── docker-compose.yml
├── .env.example
└── README.md
```

### 1.2 配置Docker Compose
创建docker-compose.yml，包含：
- Neo4j 5.x（图数据库，端口7474/7687）
- PostgreSQL 16（关系数据库，端口5432）
- MinIO（对象存储，端口9000/9001）
- 健康检查配置
- 数据卷持久化

### 1.3 初始化后端项目
- FastAPI基础框架搭建
- 项目结构创建（routers/services/models/schemas）
- 配置管理（pydantic-settings，从.env读取）
- 数据库连接管理（Neo4j + PostgreSQL）
- 健康检查API端点
- CORS配置

### 1.4 初始化前端项目
- Vite + React 18 + TypeScript
- Ant Design 5配置
- 路由配置（react-router-dom v6）
- 状态管理（zustand）
- API服务层（axios）
- 基础布局组件

### 1.5 环境配置
- .env.example（环境变量模板）
- .gitignore
- README.md（项目说明）

**任务清单**：
- [ ] 1.5.1 创建项目根目录配置文件（.env.example, .gitignore, README.md）
- [ ] 1.5.2 创建docker-compose.yml
- [ ] 1.5.3 创建后端项目结构和Dockerfile
- [ ] 1.5.4 创建后端核心配置（settings, database）
- [ ] 1.5.5 创建后端健康检查API
- [ ] 1.5.6 创建前端项目（Vite + React）
- [ ] 1.5.7 配置Ant Design和路由
- [ ] 1.5.8 创建前端基础布局
- [ ] 1.5.9 验证Docker服务启动

**交付物**：
- [ ] docker-compose.yml 可启动所有服务
- [ ] 后端Hello World API（/api/health）
- [ ] 前端基础页面（带Ant Design布局）
- [ ] 项目README文档

---

## 阶段2：知识图谱构建
**目标**：构建法语知识图谱数据模型并导入初始数据

### 2.1 设计Neo4j数据模型
```cypher
// 节点类型
(:KnowledgePoint {id, name, level, type, category})
(:Exercise {id, difficulty, type, content})
(:Lesson {id, title, level})

// 关系类型
(:KnowledgePoint)-[:PREREQUISITE_OF]->(:KnowledgePoint)
(:KnowledgePoint)-[:BELONGS_TO]->(:Lesson)
(:Exercise)-[:TESTS]->(:KnowledgePoint)
```

### 2.2 构建法语知识体系
- **词汇**：3000核心词汇（按主题/难度分级）
- **语法**：500语法点（含前置依赖关系）
- **变位**：300+动词变位形式
- **性数配合**：名词·冠词·形容词·过去分词

### 2.3 创建数据导入脚本
- 从JSON/CSV导入知识节点
- 建立前置依赖关系
- 验证图谱完整性

**交付物**：
- [ ] Neo4j数据模型文档
- [ ] 知识图谱初始数据（JSON格式）
- [ ] 数据导入脚本

---

## 阶段3：核心后端服务
**目标**：实现知识图谱服务、知识追踪服务、推荐引擎

### 3.1 知识图谱服务
```python
# 核心功能
- get_prerequisites(node_id)      # 获取前置知识
- find_learning_path(current, target)  # 查找学习路径
- get_knowledge_points(level)     # 获取某级别知识点
- get_prerequisite_chain(node_id) # 获取完整前置链
```

### 3.2 知识追踪服务（BKT）
```python
# 使用pyBKT库
- initialize_learner()            # 初始化学习者状态
- update_mastery(kp_id, correct)  # 更新掌握概率
- predict_next(learner_state)     # 预测下次表现
```

### 3.3 推荐引擎
```python
# 融合推荐策略
- kg_recommend(state, n)          # 知识图谱路径推荐
- cf_recommend(learner_id, n)     # 协同过滤推荐
- fusion_rank(kg_recs, cf_recs)   # 融合排序
- generate_reason(state, kp)      # 生成推荐理由
```

### 3.4 薄弱点诊断
```python
# 根因分析
- analyze_error(error_type)       # 分析错误类型
- root_cause_analysis(error, state)  # 根因分析
- generate_report(learner_id)     # 生成诊断报告
```

### 3.5 API路由设计
```
POST /api/learners              # 创建学习者
GET  /api/learners/{id}/state   # 获取学习状态
POST /api/recommend             # 获取推荐
POST /api/exercises/submit      # 提交练习答案
GET  /api/diagnostics/{id}      # 获取诊断报告
GET  /api/knowledge-graph       # 获取图谱数据
```

**交付物**：
- [ ] 知识图谱服务API
- [ ] BKT知识追踪服务
- [ ] 推荐引擎API
- [ ] 薄弱点诊断API

---

## 阶段4：前端核心页面
**目标**：实现学习者交互界面

### 4.1 页面结构
```
/                    # 首页/仪表板
/learning            # 学习页面
/exercises           # 练习页面
/diagnostics         # 诊断报告
/knowledge-graph     # 知识图谱可视化
/profile             # 学习者档案
```

### 4.2 核心组件
- **KnowledgeGraph**: D3.js力导向图可视化
- **ExerciseCard**: 练习题卡片组件
- **ProgressChart**: 学习进度图表
- **DiagnosticMap**: 薄弱点地图
- **RecommendationList**: 推荐列表

### 4.3 知识图谱可视化
- D3.js力导向图
- 节点颜色：红色（薄弱）/黄色（学习中）/绿色（已掌握）
- 点击节点查看详细信息
- 支持缩放和拖拽

**交付物**：
- [ ] 响应式布局框架
- [ ] 知识图谱可视化组件
- [ ] 练习界面
- [ ] 诊断报告页面

---

## 阶段5：智能功能集成
**目标**：集成NLP和LLM能力

### 5.1 CamemBERT集成
- 文本语义相似度评估（翻译题评分）
- 命名实体识别（语法分析）
- 文本分类（错误类型识别）

### 5.2 Ollama LLM集成
- 学习对话辅导
- 推荐理由生成
- 个性化解释生成

### 5.3 自适应测试（CAT）
- 题目信息量计算
- 能力估计更新
- 终止条件判断

**交付物**：
- [ ] CamemBERT文本分析服务
- [ ] LLM对话辅导功能
- [ ] CAT自适应测试

---

## 阶段6：数据与资源管理
**目标**：实现教学资源管理和数据持久化

### 6.1 PostgreSQL数据模型
```sql
-- 学习者表
CREATE TABLE learners (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    level VARCHAR(10),
    created_at TIMESTAMP
);

-- 学习记录表
CREATE TABLE learning_records (
    id UUID PRIMARY KEY,
    learner_id UUID REFERENCES learners(id),
    knowledge_point_id VARCHAR(50),
    correct BOOLEAN,
    response_time_ms INT,
    created_at TIMESTAMP
);

-- 练习记录表
CREATE TABLE exercise_records (
    id UUID PRIMARY KEY,
    learner_id UUID REFERENCES learners(id),
    exercise_id VARCHAR(50),
    answer TEXT,
    is_correct BOOLEAN,
    score FLOAT,
    created_at TIMESTAMP
);
```

### 6.2 MinIO资源管理
- 音频资源（听力练习）
- 图片资源（阅读理解）
- 文档资源（课程材料）

### 6.3 数据导入导出
- 批量导入学习者数据
- 导出学习分析报告
- 数据备份与恢复

**交付物**：
- [ ] PostgreSQL数据模型
- [ ] 数据迁移脚本
- [ ] 资源上传/下载API

---

## 阶段7：测试与优化
**目标**：确保系统质量和性能

### 7.1 单元测试
- 后端服务单元测试
- 前端组件测试
- API接口测试

### 7.2 集成测试
- 端到端测试
- 数据库集成测试
- 第三方服务集成测试

### 7.3 性能测试
- API响应时间 < 2s
- 并发支持100用户
- 图谱查询 < 50ms

### 7.4 安全测试
- 数据加密（AES-256）
- 访问权限控制
- 输入验证

**交付物**：
- [ ] 测试用例文档
- [ ] 性能测试报告
- [ ] 安全审计报告

---

## 阶段8：部署与文档
**目标**：完成生产部署和项目文档

### 8.1 生产部署
- Docker Compose生产配置
- Nginx反向代理配置
- SSL证书配置
- 日志收集配置

### 8.2 项目文档
- API文档（FastAPI自动生成）
- 部署文档
- 用户手册
- 开发者文档

### 8.3 实验准备
- 准备对照实验方案
- 设计评估问卷
- 准备DELF模拟试题

**交付物**：
- [ ] 生产部署配置
- [ ] 完整项目文档
- [ ] 实验方案文档

---

## 技术栈确认

| 层级 | 技术 | 版本 |
|:--|:--|:--|
| 前端 | React + TypeScript + Ant Design | 18.x + 5.x |
| 图谱可视化 | D3.js | 7.x |
| 后端 | FastAPI + Python | 0.110+ / 3.11+ |
| 知识图谱 | Neo4j + neo4j Python driver | 5.x / 6.x |
| 知识追踪 | pyBKT | 最新版 |
| NLP | CamemBERT (transformers) | 最新版 |
| LLM | Ollama + Qwen2.5 | 最新版 |
| 关系数据库 | PostgreSQL + SQLAlchemy | 16 / 2.0 |
| 对象存储 | MinIO | 最新版 |
| 部署 | Docker Compose | 2.x |

---

## 实施顺序建议

**推荐从阶段1开始**，按顺序执行：
1. 先搭建基础设施（Docker + 数据库）
2. 构建知识图谱数据
3. 实现后端核心服务
4. 开发前端界面
5. 集成AI功能
6. 测试优化
7. 部署上线

每个阶段完成后进行验收，确保功能可用再进入下一阶段。
