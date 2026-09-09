# 开发指南

## 目录

- [环境要求](#环境要求)
- [项目结构](#项目结构)
- [本地开发](#本地开发)
- [代码规范](#代码规范)
- [Git工作流](#git工作流)
- [测试](#测试)
- [常见问题](#常见问题)

---

## 环境要求

### 必需软件

| 软件 | 版本 | 说明 |
|:--|:--|:--|
| Docker Desktop | 最新版 | 容器化部署 |
| Node.js | 18+ | 前端开发 |
| Python | 3.11+ | 后端开发 |
| Git | 2.30+ | 版本控制 |

### 可选软件

| 软件 | 用途 |
|:--|:--|
| VS Code | 推荐IDE |
| DBeaver | 数据库管理 |
| Neo4j Browser | 图数据库可视化 |

---

## 项目结构

```
iFrenchLearning/
├── backend/                    # FastAPI后端
│   ├── app/
│   │   ├── api/routes/        # API路由
│   │   ├── core/              # 核心配置
│   │   ├── models/            # 数据模型
│   │   ├── schemas/           # Pydantic模式
│   │   └── services/          # 业务逻辑
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                   # React前端
│   ├── src/
│   │   ├── components/        # 组件
│   │   ├── pages/             # 页面
│   │   ├── services/          # API服务
│   │   ├── stores/            # 状态管理
│   │   └── types/             # 类型定义
│   └── package.json
├── knowledge-graph/            # 知识图谱
│   ├── data/                  # JSON数据
│   └── scripts/               # 导入脚本
├── docs/                       # 项目文档
├── docker-compose.yml          # Docker编排
└── .env.example                # 环境变量模板
```

---

## 本地开发

### 1. 克隆项目

```bash
git clone git@github.com:liubin18911671739/iFrenchLearning.git
cd iFrenchLearning
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，设置密码等配置
```

### 3. 启动Docker服务

```bash
docker compose up -d
```

等待服务启动（约1-2分钟）：
- Neo4j: http://localhost:7474
- PostgreSQL: localhost:5432
- MinIO: http://localhost:9001

### 4. 导入知识图谱数据

```bash
cd knowledge-graph/scripts
pip install neo4j
python import_to_neo4j.py
```

### 5. 启动后端开发服务器

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. 启动前端开发服务器

```bash
cd frontend
npm install
npm run dev
```

### 7. 访问应用

| 服务 | 地址 |
|:--|:--|
| 前端 | http://localhost:5173 |
| 后端API | http://localhost:8000 |
| API文档 | http://localhost:8000/docs |
| Neo4j Browser | http://localhost:7474 |
| MinIO Console | http://localhost:9001 |

---

## 代码规范

### Python (后端)

- 遵循 PEP 8 规范
- 使用 Black 格式化代码
- 使用 isort 排序导入
- 类型注解：使用 Python 3.11+ 类型语法

```bash
# 格式化代码
black .
isort .
```

### TypeScript (前端)

- 遵循 ESLint 配置
- 使用 Prettier 格式化
- 组件使用函数式组件 + Hooks

```bash
# 格式化代码
npm run lint
```

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**类型 (type):**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具变动

**示例:**
```bash
git commit -m "feat(exercise): 添加自适应题库"
git commit -m "fix(bkt): 修复知识追踪算法"
git commit -m "docs: 更新API文档"
```

---

## Git工作流

### 分支策略

```
main          # 生产分支
├── develop   # 开发分支
    ├── feature/*  # 功能分支
    └── fix/*      # 修复分支
```

### 开发流程

1. 从 `develop` 创建功能分支
```bash
git checkout develop
git checkout -b feature/exercise-system
```

2. 开发并提交
```bash
git add .
git commit -m "feat(exercise): 实现练习系统"
```

3. 推送到远程
```bash
git push origin feature/exercise-system
```

4. 创建Pull Request到 `develop`

5. 代码审查并合并

---

## 测试

### 后端测试

```bash
cd backend
pytest
pytest --cov=app  # 带覆盖率
```

### 前端测试

```bash
cd frontend
npm run test
npm run test:coverage  # 带覆盖率
```

### 集成测试

```bash
# 启动完整环境
docker compose up -d

# 运行API测试
curl http://localhost:8000/api/health
```

---

## 常见问题

### Q: Docker服务启动失败

```bash
# 检查端口占用
lsof -i :7474
lsof -i :5432

# 重启Docker
docker compose down
docker compose up -d
```

### Q: Neo4j连接失败

```bash
# 检查Neo4j状态
docker compose logs neo4j

# 重置Neo4j数据
docker compose down -v
docker compose up -d
```

### Q: 前端构建失败

```bash
# 清除缓存
rm -rf node_modules
rm -rf dist
npm install
npm run build
```

### Q: Python依赖安装失败

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 相关资源

- [FastAPI文档](https://fastapi.tiangolo.com/)
- [React文档](https://react.dev/)
- [Ant Design文档](https://ant.design/)
- [Neo4j文档](https://neo4j.com/docs/)
- [D3.js文档](https://d3js.org/)
