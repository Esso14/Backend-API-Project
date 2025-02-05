from typing import Optional, List
from .task import TaskConstruct
from odmantic.bson import ObjectId
from pydantic import BaseModel
from datetime import datetime


class CourseBaseInfos(BaseModel):
    id: ObjectId
    coursename: str
    module: str
    semester: int
    startdate: int
    enddate: int
    disabled: bool


class NewCourse(BaseModel):
    coursename: str
    module: str
    semester: int
    startdate: datetime
    enddate: datetime



class CourseTaskID(BaseModel):
    course_task_id: str


class CourseTaskSet(BaseModel):
    taskset_name: str
    dueDate: datetime
    task_ids: List[str]
    lateSubAllowed: bool


class CourseTaskSetResponse(BaseModel):
    taskset_name: str
    dueDate: int
    task_ids: List[ObjectId]
    lateSubAllowed: bool


class CourseTaskSetInfos(BaseModel):
    taskset_name: str
    dueDate: int
    tasks: List[TaskConstruct]
    lateSubAllowed: bool


class Course(BaseModel):
    coursename: str
    module: str
    semester: int
    startdate: int
    enddate: int
    taskSets: Optional[List[dict]] = None
    lastmodified: int
    disabled: Optional[bool] = False


class CourseResponse(BaseModel):
    id: str
    coursename: str
    module: str
    semester: int
    startdate: int
    enddate: int
    taskSets: Optional[List[CourseTaskSetInfos]] = None
    lastmodified: int
    disabled: Optional[bool] = False


class CourseRequest(BaseModel):
    coursename: str
    module: str
    semester: int
    startdate: datetime
    enddate: datetime
    taskSets: Optional[List[CourseTaskSet]] = None
    disabled: Optional[bool] = False


class EditCourse(BaseModel):
    coursename: Optional[str]
    module: Optional[str]
    semester: Optional[int]
    startdate: Optional[int]
    enddate: Optional[int]
    taskSets: Optional[List[str]] = None
    disabled: Optional[bool] = False


class UpdateCourse(BaseModel):
    coursename: Optional[str] = None
    module: Optional[str] = None
    semester: Optional[int] = None
    startdate: Optional[int] = 0
    enddate: Optional[int] = 0
    taskSets: Optional[List[str]] = None
    disabled: Optional[bool] = False