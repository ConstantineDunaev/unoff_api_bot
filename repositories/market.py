from mysql import Connection
from schemas.market import Market, UpdateMarket, NewMarket, GetMarket
from typing import List, Optional
from json import loads, dumps


class MarketRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def create_market(self, new_market: NewMarket) -> Market:
        query = "INSERT INTO t_market (name, headers, cookies, is_active, updated_at) VALUES (%s, %s, %s, %s, %s)"
        values = new_market.as_tuple()
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, values)
            return Market(market_id=cursor.lastrowid,
                          name=new_market.name,
                          headers=new_market.headers,
                          cookies=new_market.cookies,
                          is_active=new_market.is_active,
                          updated_at=new_market.updated_at)

    async def get_markets(self) -> List[Market]:
        query = ("SELECT market_id, name, ifnull(headers, '{}'), ifnull(cookies, '{}'), is_active, updated_at "
                 "FROM t_market WHERE is_active = True")
        result = []
        async with self.connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()
            for row in rows:
                result.append(Market(market_id=row[0],
                                     name=row[1],
                                     headers=loads(row[2]),
                                     cookies=loads(row[3]),
                                     is_active=row[4],
                                     updated_at=row[5]))
        return result

    async def get_market(self, get_market: GetMarket) -> Optional[Market]:
        query = ("SELECT market_id, name, ifnull(headers, '{}'), ifnull(cookies, '{}'), is_active, updated_at "
                 "FROM t_market WHERE market_id = %s LIMIT 1")
        values = get_market.as_tuple()
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, values)
            row = await cursor.fetchone()
            if not row:
                return None
            return Market(market_id=row[0],
                          name=row[1],
                          headers=loads(row[2]),
                          cookies=loads(row[3]),
                          is_active=row[4],
                          updated_at=row[5])

    async def update_market(self, update_market: UpdateMarket) -> Market:
        query = ("UPDATE t_market SET name = %s, headers = %s, cookies = %s, is_active = %s, updated_at = %s "
                 "WHERE market_id = %s")
        values = update_market.as_tuple()
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, values)
            return Market(market_id=update_market.market_id,
                          name=update_market.name,
                          headers=update_market.headers,
                          cookies=update_market.cookies,
                          is_active=update_market.is_active,
                          updated_at=update_market.updated_at)
