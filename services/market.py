from repositories.market import MarketRepository
from db import Connection
from typing import List
from schemas.market import Market, NewMarket
from utils.curl import parse_curl
from datetime import datetime


async def get_markets(connection: Connection) -> List[Market]:
    market_repo = MarketRepository(connection)
    return await market_repo.get_markets()


async def create_market(connection: Connection, name: str, curl: str) -> Market:
    headers, cookies = parse_curl(curl)
    new_market = NewMarket(name=name,
                           headers=headers,
                           cookies=cookies,
                           is_active=True,
                           updated_at=datetime.now())
    market_repo = MarketRepository(connection)
    return await market_repo.create_market(new_market)

