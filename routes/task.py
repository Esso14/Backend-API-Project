from fastapi import APIRouter
from datetime import datetime
from settings import engine
from schemas.task import NewTask
from models.task import TaskModel



router = APIRouter()

# New task
@router.post("/task/new/", response_model=TaskModel)
async def create_task(task: NewTask):

    taskdoc = TaskModel(
        name=task.name,
        topics=task.topics,
        exercise=task.exercise,
        exerciseImage=task.exerciseImage,
        ancestorTaskId=task.ancestorTaskId,
        creationdate=int(datetime.now().timestamp()),
        lastmodified=int(datetime.now().timestamp()),
        # disabled=task.disabled,
    )
    await engine.save(taskdoc)
    return taskdoc
