# 部署指南

## 目录

- [部署架构](#部署架构)
- [环境要求](#环境要求)
- [Docker部署](#docker部署)
- [生产环境配置](#生产环境配置)
- [Nginx配置](#nginx配置)
- [数据备份](#数据备份)
- [监控与日志](#监控与日志)
- [常见问题](#常见问题)

---

## 部署架构

```
                    ┌─────────────────┐
                    │   用户浏览器     │
                    └────────┬────────┘
                             │ HTTPS
                    ┌────────▼────────┐
                    │     Nginx       │
                    │  (反向代理)      │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
    │   Frontend  │  │   Backend   │  │    MinIO    │
    │   (静态)    │  │  (FastAPI)  │  │  (资源存储)  │
    └─────────────┘  └──────┬──────┘  └─────────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       ┌──────▼──────┐ ┌───▼────┐ ┌──────▼──────┐
       │    Neo4j    │ │PostgreSQL│ │   Ollama    │
       │  (图数据库)  │ │(关系数据) │ │  (本地LLM)  │
       └─────────────┘ └────────┘ └─────────────┘
```

---

## 环境要求

### 硬件配置

| 配置 | 最低要求 | 推荐配置 |
|:--|:--|:--|
| CPU | 8核 | 16核 |
| 内存 | 32GB | 64GB |
| 存储 | 500GB SSD | 1TB SSD |
| GPU | RTX 3090 24GB | RTX 4090 24GB |

### 软件要求

| 软件 | 版本 |
|:--|:--|
| Docker | 24.0+ |
| Docker Compose | 2.20+ |
| Nginx | 1.24+ (可选) |

---

## Docker部署

### 1. 准备环境

```bash
# 克隆代码
git clone git@github.com:liubin18911671739/iFrenchLearning.git
cd iFrenchLearning

# 配置环境变量
cp .env.example .env
```

### 2. 编辑环境变量

```bash
vim .env
```

修改以下配置：

```env
# 数据库密码（必须修改）
NEO4J_PASSWORD=your_secure_password
POSTGRES_PASSWORD=your_secure_password

# 应用密钥（必须修改）
APP_SECRET_KEY=your_random_secret_key
```

### 3. 启动服务

```bash
# 构建并启动
docker compose up -d --build

# 查看状态
docker compose ps

# 查看日志
docker compose logs -f api
```

### 4. 导入知识图谱

```bash
# 进入后端容器
docker compose exec api bash

# 安装依赖
pip install neo4j

# 导入数据
cd /app/../knowledge-graph/scripts
python import_to_neo4j.py
```

### 5. 验证部署

```bash
# 检查API健康
curl http://localhost:8000/api/health

# 检查Neo4j
curl http://localhost:7474

# 检查MinIO
curl http://localhost:9001
```

---

## 生产环境配置

### 1. 创建生产环境配置文件

```bash
cp docker-compose.yml docker-compose.prod.yml
```

### 2. 修改生产配置

编辑 `docker-compose.prod.yml`：

```yaml
services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production
    environment:
      - APP_ENV=production
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  neo4j:
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
    volumes:
      - neo4j_data:/data
    deploy:
      resources:
        limits:
          memory: 16G

  postgres:
    volumes:
      - postgres_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          memory: 8G
```

### 3. 生产环境启动

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## Nginx配置

### 1. 创建Nginx配置

```bash
mkdir -p nginx/conf.d
```

编辑 `nginx/conf.d/default.conf`：

```nginx
upstream api {
    server api:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API代理
    location /api/ {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # MinIO代理
    location /minio/ {
        proxy_pass http://minio:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. SSL证书配置

```bash
# 使用Let's Encrypt
certbot certonly --webroot -w /var/www/html -d your-domain.com

# 或者使用自签名证书
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx/ssl/key.pem \
    -out nginx/ssl/cert.pem
```

---

## 数据备份

### Neo4j备份

```bash
# 备份
docker compose exec neo4j neo4j-admin database dump neo4j --to-path=/backups/neo4j.dump

# 恢复
docker compose exec neo4j neo4j-admin database load neo4j --from-path=/backups/neo4j.dump
```

### PostgreSQL备份

```bash
# 备份
docker compose exec postgres pg_dump -U postgres ifrench > backup.sql

# 恢复
docker compose exec -T postgres psql -U postgres ifrench < backup.sql
```

### MinIO备份

```bash
# 安装mc客户端
docker run --rm -v ~/minio:/root/.mc minio/mc alias set local http://minio:9000 minioadmin minioadmin

# 备份
docker run --rm -v ~/minio:/root/.mc -v ~/backup:/backup minio/mc mirror local/ifrench-resources /backup
```

### 自动备份脚本

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/$DATE"

mkdir -p $BACKUP_DIR

# Neo4j备份
docker compose exec -T neo4j neo4j-admin database dump neo4j --to-path=/tmp/neo4j.dump
docker compose cp neo4j:/tmp/neo4j.dump $BACKUP_DIR/

# PostgreSQL备份
docker compose exec -T postgres pg_dump -U postgres ifrench > $BACKUP_DIR/postgres.sql

# 压缩
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR

echo "备份完成: $BACKUP_DIR.tar.gz"
```

---

## 监控与日志

### 查看服务状态

```bash
# 查看所有服务状态
docker compose ps

# 查看资源使用
docker stats

# 查看特定服务日志
docker compose logs -f api
docker compose logs -f neo4j
```

### 健康检查

```bash
# API健康检查
curl -f http://localhost:8000/api/health || exit 1

# Neo4j健康检查
curl -f http://localhost:7474 || exit 1

# PostgreSQL健康检查
docker compose exec postgres pg_isready -U postgres
```

### 日志管理

```bash
# 清理旧日志
docker system prune -a

# 查看Docker日志
docker compose logs --tail=100 api
```

---

## 常见问题

### Q: 服务启动后无法访问

```bash
# 检查端口占用
netstat -tulpn | grep -E '(8000|7474|5432|9000)'

# 检查防火墙
sudo ufw status

# 检查Docker网络
docker network ls
docker network inspect ifrench-learning_ifrench-network
```

### Q: 内存不足

```bash
# 查看内存使用
docker stats --no-stream

# 增加Docker内存限制
# Docker Desktop -> Settings -> Resources -> Memory
```

### Q: 数据库连接失败

```bash
# 检查数据库日志
docker compose logs postgres
docker compose logs neo4j

# 重启数据库
docker compose restart postgres neo4j
```

### Q: 如何更新应用

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker compose up -d --build

# 或者只更新特定服务
docker compose up -d --build api
```

---

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|:--|:--|:--|
| NEO4J_URI | Neo4j连接地址 | bolt://neo4j:7687 |
| NEO4J_USERNAME | Neo4j用户名 | neo4j |
| NEO4J_PASSWORD | Neo4j密码 | - |
| POSTGRES_HOST | PostgreSQL主机 | postgres |
| POSTGRES_PORT | PostgreSQL端口 | 5432 |
| POSTGRES_USER | PostgreSQL用户 | postgres |
| POSTGRES_PASSWORD | PostgreSQL密码 | - |
| POSTGRES_DB | 数据库名 | ifrench |
| MINIO_ENDPOINT | MinIO地址 | minio:9000 |
| MINIO_ACCESS_KEY | MinIO访问密钥 | minioadmin |
| MINIO_SECRET_KEY | MinIO密钥 | minioadmin |
| OLLAMA_BASE_URL | Ollama地址 | http://ollama:11434 |
| APP_ENV | 环境 | development |
| APP_SECRET_KEY | 应用密钥 | - |
| CORS_ORIGINS | CORS来源 | http://localhost:5173 |
