from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "iFrench Learning API",
    }


@router.get("/health/neo4j")
async def neo4j_health_check():
    """Neo4j连接检查"""
    from app.core.database import neo4j_driver

    try:
        async with neo4j_driver.session() as session:
            result = await session.run("RETURN 1 as n")
            record = await result.single()
            return {"status": "healthy", "database": "neo4j", "result": record["n"]}
    except Exception as e:
        return {"status": "unhealthy", "database": "neo4j", "error": str(e)}


@router.get("/health/postgres")
async def postgres_health_check():
    """PostgreSQL连接检查"""
    from sqlalchemy import text
    from app.core.database import PostgresSessionLocal

    try:
        async with PostgresSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "postgres", "result": result.scalar()}
    except Exception as e:
        return {"status": "unhealthy", "database": "postgres", "error": str(e)}
