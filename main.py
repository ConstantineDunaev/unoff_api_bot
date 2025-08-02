from asyncio import run
from db import connection_context, db_pool
from repositories.market import MarketRepository
from repositories.job import JobRepository
from repositories.discount_wb import DiscountWBRepository
from datetime import datetime
from schemas.job import NewJob
from schemas.discount_wb import RowDiscountWB
from wildberries.get_discount_wb import get_discount_wb


async def main():
    async with db_pool:
        async with connection_context() as conn:

            market_repo = MarketRepository(conn)
            job_repo = JobRepository(conn)
            discount_wb_repo = DiscountWBRepository(conn)


            markets = await market_repo.get_markets()
            for market in markets:
                new_job = NewJob(market_id=market.market_id,
                                 start=datetime.now(),
                                 script_name='TEST')
                job = await job_repo.create_job(new_job)

                items = await get_discount_wb(headers=market.headers,
                                              cookies=market.cookies)
                rows = [RowDiscountWB(nm_id=item.nm_id,
                                      vendor_code=item.vendor_code,
                                      discount_on_site=item.discount_on_site,
                                      job_id=job.job_id)
                        for item in items]
                await discount_wb_repo.write_rows(rows)

                job.finish = datetime.now()
                await job_repo.finish_job(job)
            await conn.commit()


if __name__ == '__main__':
    run(main())
