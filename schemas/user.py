from typing import Optional, List
from pydantic import BaseModel, EmailStr
from odmantic import  Field
from odmantic.bson import ObjectId
from enum import Enum
from .course import CourseBaseInfos


class Role(str, Enum):
    student = "student"
    tutor = "tutor"
    teacher = "teacher"
    admin = "admin"


class PermissionFor(str, Enum):
    webinterface_admin = "webinterface_admin",
    app1 = "app1"
    app2 = "app2"
    task_app = "task_app"
    select = "- select -"


class UserEnrollment(BaseModel):
    course_id: ObjectId
    course_role: Role
    enroll_date: int



class UserEnrollmentModel(BaseModel):
    course_id: ObjectId
    course_role: str
    enroll_date: int


class UserBaseInfos(BaseModel):
    id: ObjectId
    username: str
    firstName: str
    lastName: str
    permissionFor: PermissionFor
    email: EmailStr
    disabled: bool


class NewUser(BaseModel):
    username: str
    firstName: str
    lastName: str
    password: str
    email: EmailStr
    photoUrls: Optional[List[str]] = None


class UserEnrollmentRequest(BaseModel):
    course_id: str  # courseId
    course_role: Role
    enroll_date: Optional[int] = 0 # Date from app as integer


class UserEnrollmentResponse(BaseModel):
    course: CourseBaseInfos  # link to course
    course_role: Role
    enroll_date: Optional[int] = 0


class UserCourseRoleUpdate(BaseModel):
    course_id: str  # courseId
    course_role: Optional[Role] = None


class UserConsentUpdate(BaseModel):
    consent_given: Optional[bool] = None


class User(BaseModel):
    username: str
    firstName: str
    lastName: str
    hash_password: str
    email: EmailStr
    permissionFor: PermissionFor
    email: EmailStr
    enrollments: Optional[List[UserEnrollment]] = None
    photoUrls: Optional[List[str]] = None
    consent_given: Optional[bool] = False
    consent_date: Optional[int] = 0
    disabled: Optional[bool] = False


class UserResponse(BaseModel):
    id: str
    username: str
    firstName: str
    lastName: str
    permissionFor: PermissionFor
    email: EmailStr
    enrollments: Optional[List[UserEnrollmentResponse]] = Field(default_factory=list)
    photoUrls: Optional[List[str]] = None
    consent_given: Optional[bool] = False
    consent_date: Optional[int] = 0
    disabled: Optional[bool] = False


class EditUser(BaseModel):
    permissionFor: Optional[PermissionFor] = None
    photoUrls: Optional[List[str]] = None
    disabled: Optional[bool] = False


class UserIn(BaseModel):
    username: str
    password: str