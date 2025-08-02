from mysql import MySQLPool
from config import Config
from contextlib import asynccontextmanager

db_pool = MySQLPool(
    host=Config.MYSQL_HOST,
    port=Config.MYSQL_PORT,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    db=Config.MYSQL_SCHEMA
)


@asynccontextmanager
async def connection_context():
    """Контекстный менеджер для скриптов"""
    await db_pool.init_pool()
    conn = await db_pool.acquire()
    try:
        yield conn
    finally:
        await db_pool.release(conn)


async def get_connection():
    """Dependency для FastAPI"""
    async with connection_context() as conn:
        yield conn
