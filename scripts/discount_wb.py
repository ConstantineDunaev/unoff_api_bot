from asyncio import run
from db import connection_context, Connection
from repositories.market import MarketRepository
from repositories.job import JobRepository
from datetime import datetime
from schemas.job import NewJob
from services.discount_wb import process_discount_wb
from asyncio import create_task, gather
from schemas.market import Market
from typing import Optional, Callable, List, Coroutine
from aiogram import Bot


async def run_script(connection: Connection, bot: Bot, func: Callable, caption: str):
    job_repo = JobRepository(connection)
    market_repo = MarketRepository(connection)

    async def handle(market: Market):
        new_job = NewJob(market_id=market.market_id,
                         start=datetime.now(),
                         script_name=caption)
        job = await job_repo.create_job(new_job)

        job.result = await func(connection=connection,
                                headers=market.headers,
                                cookies=market.cookies,
                                job=job)
        job.finish = datetime.now()
        await job_repo.finish_job(job)

    markets = await market_repo.get_markets()
    tasks = [create_task(handle(market)) for market in markets]
    await gather(*tasks)


async def discount_wb1():
    async with connection_context() as connection:
        market_repo = MarketRepository(connection)
        job_repo = JobRepository(connection)

        markets = await market_repo.get_markets()
        tasks = []
        for market in markets:
            new_job = NewJob(market_id=market.market_id,
                             start=datetime.now(),
                             script_name='TEST')
            job = await job_repo.create_job(new_job)

            finished_job = await process_discount_wb(connection=connection,
                                                     headers=market.headers,
                                                     cookies=market.cookies,
                                                     job=job)
            await job_repo.finish_job(finished_job)


if __name__ == '__main__':
    run(discount_wb())
