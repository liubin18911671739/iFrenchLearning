from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import api_router
from app.core.database import init_db

app = FastAPI(
    title="iFrench Learning API",
    description="基于知识图谱的法语自适应智能学习系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库连接"""
    await init_db()


@app.get("/")
async def root():
    return {
        "name": "iFrench Learning API",
        "version": "1.0.0",
        "docs": "/docs",
    }
