import functools
from datetime import datetime
from schemas.job import NewJob
from aiogram import Bot


def job_wrapper(script_name: str, bot: Bot, users: set):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*, conn, market, job_repo, **kwargs):
            new_job = NewJob(
                market_id=market.market_id,
                start=datetime.now(),
                script_name=script_name
            )
            job = await job_repo.create_job(new_job)

            try:
                job.result = await func(connection=conn, job=job, **kwargs)
            except Exception as e:
                job.result = f"Ошибка: {e}"
                raise
            finally:
                job.finish = datetime.now()
                await job_repo.finish_job(job)

            return job
        return wrapper
    return decorator
