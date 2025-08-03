from mysql import Connection
from schemas.market import Market, UpdateMarket, NewMarket
from typing import List
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

    async def update_market(self, update_market: UpdateMarket) -> Market:
        query = "UPDATE t_market SET name = %s, headers = %s, "
