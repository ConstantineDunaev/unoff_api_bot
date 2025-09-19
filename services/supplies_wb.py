from repositories.supply_wb import SupplyWBRepository
from wildberries.get_supplies import get_supplies_wb
from wildberries.get_supply_details import get_supply_details_wb
from schemas.job import Job
from schemas.supply_wb import RowSupplyDetailWB
from mysql import Connection
from logging import getLogger
from traceback import format_exc
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


logger = getLogger('SUPPLIES_WB')


async def process_supplies_wb(job: Job, connection: Connection, headers: dict, cookies: dict) -> Job:
    logger.info("START PROCECESSING JOB_ID = %d", job.job_id)
    min_supply_date = date.today() - relativedelta(months=1)
    logger.debug("min_supply_date = %s", min_supply_date)
    supply_wb_repo = SupplyWBRepository(connection)
    result = []
    try:
        items = await get_supplies_wb(headers=headers,
                                      cookies=cookies)
        supplies = [item for item in items if item.supply_date.date() >= min_supply_date]
        for supply in supplies:
            supply_details = await get_supply_details_wb(headers=headers,
                                                         cookies=cookies,
                                                         supply_id=supply.supply_id)
            result += [RowSupplyDetailWB(job_id=job.job_id,
                                         **detail.as_dict(),
                                         **supply.as_dict()) for detail in supply_details]
        await supply_wb_repo.write_rows(result)
        logger.info("SUCCESS JOB_ID = %d", job.job_id)
        job.result = 'OK'
    except Exception as e:
        logger.exception("ERROR JOB_ID = %d: %s", job.job_id, str(e))
        job.result = format_exc()
    job.finish = datetime.now()
    return job
