from odmantic import Model, Field
from typing import Optional, List
from starlette.requests import Request


class TaskModel(Model):
    name: Optional[str] = None
    topics: Optional[List[str]] = None
    exercise: Optional[str] = None
    exerciseImage: Optional[List[str]] = None
    ancestorTaskId: Optional[List[str]] = []
    creationdate: int
    lastmodified: int
    disabled: Optional[bool] = Field(default=False)

    async def __admin_repr__(self, request: Request):
        return f"{self.name}"
