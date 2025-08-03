from repositories.discount_wb import DiscountWBRepository
from wildberries.get_discount_wb import get_discount_wb
from schemas.job import Job
from schemas.discount_wb import RowDiscountWB
from mysql import Connection
from logging import getLogger
from traceback import format_exc
from datetime import datetime

logger = getLogger('DISCOUNT_WB')


async def process_discount_wb(job: Job, connection: Connection, headers: dict, cookies: dict) -> Job:
    logger.info("START PROCECESSING JOB_ID = %d", job.job_id)
    discount_wb_repo = DiscountWBRepository(connection)
    try:
        items = await get_discount_wb(headers=headers,
                                      cookies=cookies)
        rows = [RowDiscountWB(nm_id=item.nm_id,
                              vendor_code=item.vendor_code,
                              discount_on_site=item.discount_on_site,
                              job_id=job.job_id)
                for item in items]
        await discount_wb_repo.write_rows(rows)
        logger.info("SUCCESS JOB_ID = %d", job.job_id)
        job.result = 'OK'
    except Exception as e:
        logger.exception("ERROR JOB_ID = %d: %s", job.job_id, str(e))
        job.result = format_exc()
    job.finish = datetime.now()
    return job
