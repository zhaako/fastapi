from typing import Optional

from database import new_s, TaskOrm
from sqlalchemy import select
from schemas import STaskAdd, STask, STaskUpdate


class TaskRepository:
    @classmethod
    async def update_tasks(cls, task_id: int, updated_task_data: STaskUpdate) -> Optional[STask]:
        async with new_s() as session:
            task = await session.get(TaskOrm, task_id)
            for n, d in updated_task_data.dict(exclude_unset=True).items():
                setattr(task, n, d)

            await session.commit()
            return STask.model_validate(task)

    @classmethod
    async def add_task(cls, task: STaskAdd) -> int:
        async with new_s() as session:
            data = task.model_dump()
            new_task = TaskOrm(**data)
            session.add(new_task)
            await session.flush()
            await session.commit()
            return new_task.id

    @classmethod
    async def get_tasks(cls) -> list[STask]:
        async with new_s() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [STask.model_validate(task_model) for task_model in task_models]
            return tasks

    @classmethod
    async def delete_tasks(cls, task_id: int) -> bool:
        async with new_s() as session:
            task = await session.get(TaskOrm, task_id)
            if task is None:
                return False
            await session.delete(task)
            await session.flush()
            await session.commit()
