from odmantic import Model, Field
from starlette.requests import Request
from typing import Optional, List
import schemas.course as course_schema


class CourseModel(Model):
    coursename: str
    module: str
    semester: int
    startdate: int
    enddate: int
    taskSets: Optional[List[course_schema.CourseTaskSetResponse]] = None
    lastmodified: Optional[int] = 0
    disabled: Optional[bool] = Field(default=False)

    async def __admin_repr__(self, request: Request):
        return f"{self.coursename}"
