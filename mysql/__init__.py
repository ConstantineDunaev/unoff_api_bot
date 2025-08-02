from aiomysql import create_pool, Connection


class MySQLPool:
    def __init__(self, host, port, user, password, db, minsize=1, maxsize=10):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.minsize = minsize
        self.maxsize = maxsize
        self.pool = None

    async def init_pool(self):
        if not self.pool:
            self.pool = await create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                minsize=self.minsize,
                maxsize=self.maxsize,
                autocommit=True,
            )

    async def acquire(self):
        return await self.pool.acquire()

    async def release(self, conn):
        self.pool.release(conn)

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None

    async def __aenter__(self):
        await self.init_pool()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

