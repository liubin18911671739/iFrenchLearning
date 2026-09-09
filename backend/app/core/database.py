from neo4j import AsyncGraphDatabase, AsyncDriver
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """SQLAlchemy基类"""
    pass


# Neo4j驱动
neo4j_driver: AsyncDriver | None = None


# PostgreSQL引擎
postgres_engine = create_async_engine(
    settings.POSTGRES_DATABASE_URL,
    echo=settings.APP_ENV == "development",
    pool_pre_ping=True,
)

PostgresSessionLocal = async_sessionmaker(
    postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """初始化数据库连接"""
    global neo4j_driver

    # 初始化Neo4j连接
    neo4j_driver = AsyncGraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD),
    )
    await neo4j_driver.verify_connectivity()
    print(f"Neo4j connected: {settings.NEO4J_URI}")

    # 创建PostgreSQL表
    async with postgres_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"PostgreSQL connected: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}")


async def close_db():
    """关闭数据库连接"""
    global neo4j_driver
    if neo4j_driver:
        await neo4j_driver.close()
        print("Neo4j connection closed")
    await postgres_engine.dispose()
    print("PostgreSQL connection closed")


def get_neo4j_session():
    """获取Neo4j会话"""
    return neo4j_driver.session(database="neo4j")


async def get_postgres_session():
    """获取PostgreSQL会话（用于FastAPI依赖注入）"""
    async with PostgresSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
