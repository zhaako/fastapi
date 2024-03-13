from fastapi import APIRouter, Depends

from repository import TaskRepository
from schemas import STaskAdd, STask, STaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post("")
async def add_task(task: STaskAdd = Depends()) -> dict[str, int]:
    new_task_id = await TaskRepository.add_task(task)
    return {"id": new_task_id}


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.get_tasks()
    return tasks


@router.delete("/{task_id}")
async def delete_tasks(task_id: int) -> dict:
    await TaskRepository.delete_tasks(task_id)
    return {"message": "good"}


@router.put("/{task_id}")
async def update_task(task_id: int, updated_task: STaskUpdate) -> STask:
    updated_task = await TaskRepository.update_tasks(task_id, updated_task)
    return updated_task
