# 基于知识图谱的法语自适应智能学习系统

## 项目简介

本系统旨在根据学习者的个体差异（知识水平、学习风格、认知能力等）动态调整学习内容和路径，实现个性化法语教学。

### 核心特性

- **知识图谱驱动**：基于Neo4j构建法语知识体系，支持知识点依赖关系推理
- **自适应学习**：融合BKT知识追踪与协同过滤推荐，个性化学习路径规划
- **薄弱点诊断**：通过根因分析算法定位学习薄弱环节
- **智能辅导**：集成CamemBERT和Ollama LLM，提供AI对话辅导

### 技术栈

| 层级 | 技术 |
|:--|:--|
| 前端 | React 18 + TypeScript + Ant Design 5 + D3.js |
| 后端 | FastAPI + Python 3.11 |
| 图数据库 | Neo4j 5.x |
| 关系数据库 | PostgreSQL 16 |
| 对象存储 | MinIO |
| LLM | Ollama + Qwen2.5 |
| NLP | CamemBERT |
| 部署 | Docker Compose |

## 快速开始

### 前置要求

- Docker Desktop (最新版)
- Node.js 18+ (前端开发)
- Python 3.11+ (后端开发)

### 1. 克隆项目

```bash
git clone <repository-url>
cd iFrenchLearning
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，设置数据库密码等配置
```

### 3. 启动Docker服务

```bash
docker compose up -d
```

等待所有服务启动完成（约1-2分钟）。

### 4. 启动后端开发服务器

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 启动前端开发服务器

```bash
cd frontend
npm install
npm run dev
```

### 6. 访问应用

- **前端**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
- **MinIO Console**: http://localhost:9001

## 项目结构

```
iFrenchLearning/
├── frontend/              # React前端应用
│   ├── src/
│   │   ├── components/    # 可复用组件
│   │   ├── pages/         # 页面组件
│   │   ├── services/      # API服务层
│   │   ├── stores/        # 状态管理
│   │   └── utils/         # 工具函数
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI后端服务
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── core/          # 核心配置
│   │   ├── models/        # 数据模型
│   │   ├── schemas/       # Pydantic模式
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   ├── requirements.txt
│   └── Dockerfile
├── knowledge-graph/       # 知识图谱数据
│   ├── data/              # JSON数据文件
│   └── scripts/           # 导入脚本
├── docker-compose.yml     # Docker编排配置
├── .env.example           # 环境变量模板
└── README.md
```

## 功能模块

### 1. 学习者建模
- 知识维度：基于BKT模型追踪知识点掌握状态
- 认知维度：基于布鲁姆认知分类法评估能力水平
- 行为维度：追踪学习行为模式

### 2. 自适应推荐
- 知识图谱路径推荐
- 协同过滤推荐
- 深度强化学习推荐
- 冷启动先验推荐

### 3. 薄弱点诊断
- 错误模式识别
- 根因分析算法
- 可视化诊断报告

### 4. 智能练习
- 自适应题库（IRT标定）
- 动态组卷算法
- 即时反馈机制
- 计算机自适应测试（CAT）

## 开发指南

### 代码规范

- **Python**: 遵循PEP 8，使用Black格式化
- **TypeScript**: 遵循ESLint配置
- **Git**: 使用Conventional Commits规范

### 分支管理

- `main`: 生产分支
- `develop`: 开发分支
- `feature/*`: 功能分支
- `fix/*`: 修复分支

### 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm run test
```

## 部署

### 生产环境

```bash
# 构建并启动
docker compose -f docker-compose.prod.yml up -d --build

# 查看日志
docker compose logs -f api
```

## 许可证

本项目仅用于学术研究目的。

## 联系方式

如有问题，请提交Issue或联系项目维护者。
# iFrenchLearning
