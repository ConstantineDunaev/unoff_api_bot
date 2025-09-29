from db import Connection
from repositories.market import MarketRepository
from repositories.job import JobRepository
from datetime import datetime
from schemas.job import NewJob
from typing import Callable, Set
from aiogram import Bot
from resources import Texts


async def run_script(connection: Connection, bot: Bot, func: Callable, caption: str, users: Set[int]):
    job_repo = JobRepository(connection)
    market_repo = MarketRepository(connection)

    markets = await market_repo.get_markets()
    results = []
    if markets:
        for market in markets:
            new_job = NewJob(market_id=market.market_id,
                             start=datetime.now(),
                             script_name=caption)
            job = await job_repo.create_job(new_job)

            finished_job = await func(connection=connection,
                                      headers=market.headers,
                                      cookies=market.cookies,
                                      market=market,
                                      job=job)
            await job_repo.finish_job(finished_job)
            text = Texts.market_result.format(market_name=market.name,
                                              job_id=job.job_id,
                                              result=job.result)
            results.append(text)

        markets_result = '\n\n'.join(results)
        text = Texts.script_result.format(markets_result=markets_result,
                                          caption=caption)
        for user_id in users:
            await bot.send_message(chat_id=user_id,
                                   text=text)



