import datetime
from typing import List, Optional

from repositories.base import BaseRepository
from models.jobs import JobIn, Job
from db.jobs import jobs


class JobRepository(BaseRepository):

    async def create(self, user_id: int, j: JobIn) -> Job:
        creating_job = Job(
            user_id=user_id,
            title=j.title,
            description=j.description,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            is_active=j.is_active,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        values = {**creating_job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        creating_job.id = await self.database.execute(query)
        return creating_job

    async def update(self, id: int, user_id: int, j: JobIn) -> Job:
        updating_job = Job(
            id=id,
            user_id=user_id,
            title=j.title,
            description=j.description,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            is_active=j.is_active,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**updating_job.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = jobs.update().where(jobs.c.id == id).values(**values)
        await self.database.execute(query)
        return updating_job

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[Job]:
        query = jobs.select().limit(limit).offset(skip)
        jobs_list = await self.database.fetch_all(query)
        return jobs_list

    async def get_by_id(self, id: int) -> Optional[Job]:
        query = jobs.select().where(jobs.c.id == id)
        job = await self.database.fetch_one(query)
        if job is None:
            return None
        return Job.parse_obj(job)

    async def delete(self, id: int):
        query = jobs.delete().where(jobs.c.id == id)
        return await self.database.execute(query)
