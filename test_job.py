from asyncio import run
from db import connection_context
from repositories.market import MarketRepository
from repositories.job import JobRepository
from datetime import datetime
from schemas.job import NewJob
from services.discount_wb import process_discount_wb


async def main():
    async with connection_context() as conn:
        market_repo = MarketRepository(conn)
        job_repo = JobRepository(conn)

        markets = await market_repo.get_markets()
        for market in markets:
            new_job = NewJob(market_id=market.market_id,
                             start=datetime.now(),
                             script_name='TEST')
            job = await job_repo.create_job(new_job)

            job.result = await process_discount_wb(connection=conn,
                                                   headers=market.headers,
                                                   cookies=market.cookies,
                                                   job=job)
            job.finish = datetime.now()
            await job_repo.finish_job(job)
        await conn.commit()


if __name__ == '__main__':
    run(main())
