from mysql import MySQLPool, Connection
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
    async with db_pool:
        conn = await db_pool.acquire()
        try:
            yield conn
        finally:
            await db_pool.release(conn)


async def init_database(dump_path: str):
    with open(dump_path, 'r', encoding='UTF-8') as f:
        queries = [query.strip() for query in f.read().strip().split(';') if query.strip()]
    async with connection_context() as connection:
        async with connection.cursor() as cursor:
            for query in queries:
                await cursor.execute(query)
