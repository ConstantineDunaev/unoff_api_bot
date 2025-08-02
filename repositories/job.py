from mysql import Connection
from schemas.job import Job, NewJob


class JobRepository:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def create_job(self, new_job: NewJob) -> Job:
        query = "INSERT INTO t_job (market_id, script, start, params) VALUES (%s, %s, %s, %s)"
        values = (new_job.market_id, new_job.script_name, new_job.start, new_job.params)
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, values)
            return Job(job_id=cursor.lastrowid,
                       market_id=new_job.market_id,
                       script_name=new_job.script_name,
                       start=new_job.start,
                       params=new_job.params)

    async def finish_job(self, job: Job):
        query = "UPDATE t_job SET finish = %s WHERE job_id = %s"
        values = (job.finish, job.job_id)
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, values)
