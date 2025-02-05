from pydantic import BaseModel
from typing import Optional, List
from odmantic.bson import ObjectId




class TaskConstruct(BaseModel):
    id: ObjectId
    name: str
    topics: List[str]
    exercise: str
    exerciseImage: Optional[List[str]]
    disabled: bool


class Task(BaseModel):
    name: str
    topics: List[str]
    exercise: str
    exerciseImage: Optional[List[str]]
    ancestorTaskId: Optional[List[str]] = None
    creationdate: Optional[int] = 0
    lastmodified: int
    disabled: Optional[bool] = False


class NewTask(BaseModel):
    name: str
    topics: List[str]
    exercise: str
    exerciseImage: Optional[List[str]]
    ancestorTaskId: Optional[List[str]] = None


class TaskResponse(BaseModel):
    id: str
    task: Task


class TaskWithId(Task):
    id: ObjectId


class UpdateTask(BaseModel):
    name: Optional[str] = None
    topics: Optional[List[str]] = None
    exercise: Optional[str] = None
    exerciseImage: Optional[List[str]] = None
    ancestorTaskId: Optional[List[str]] = None
    disabled: Optional[bool] = False


class EditTask(BaseModel):
    name: Optional[str]
    topics: Optional[List[str]]
    exercise: Optional[str]
    exerciseImage: Optional[List[str]] = None
    ancestorTaskId: Optional[List[str]]
    disabled: Optional[bool] = False


class TaskUpdateResponse(TaskConstruct):
    taskt: TaskWithId
