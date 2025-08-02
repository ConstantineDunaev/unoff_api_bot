from mysql import Connection
from schemas.market import Market
from typing import List
from json import loads, dumps


class MarketRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def get_markets(self) -> List[Market]:
        query = ("SELECT market_id, name, headers, cookies, is_active, updatet_at "
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
                                     updatet_at=row[5]))
        return result

