from repositories.market import MarketRepository
from db import Connection
from typing import List
from schemas.market import Market, NewMarket, UpdateMarket, GetMarket


async def get_markets(connection: Connection) -> List[Market]:
    market_repo = MarketRepository(connection)
    return await market_repo.get_markets()


async def get_market(connection: Connection, get_market_: GetMarket) -> Market:
    market_repo = MarketRepository(connection)
    return await market_repo.get_market(get_market_)


async def create_market(connection: Connection, new_market: NewMarket) -> Market:
    market_repo = MarketRepository(connection)
    return await market_repo.create_market(new_market)


async def update_market(connection: Connection, upd_market: UpdateMarket) -> Market:
    market_repo = MarketRepository(connection)
    return await market_repo.update_market(upd_market)

