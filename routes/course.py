from fastapi import APIRouter
from models.course import CourseModel
from schemas.course import NewCourse
from settings import engine
from datetime import datetime



router = APIRouter()


@router.post("/courses/new/", response_model=CourseModel)
async def create_course(course: NewCourse):

    # Konvertiere die datetime-Felder in Timestamps
    startdate_timestamp = int(course.startdate.timestamp())
    enddate_timestamp = int(course.enddate.timestamp())

    course_instance = CourseModel(
        coursename=course.coursename,
        module=course.module,
        semester=course.semester,
        startdate=startdate_timestamp,
        enddate=enddate_timestamp,
        lastmodified=int(datetime.now().timestamp())
    )
    await engine.save(course_instance)
    return course_instance


