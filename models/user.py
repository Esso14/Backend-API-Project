from typing import Optional, List
from pydantic import EmailStr
from odmantic import Model, Field
from datetime import datetime
import schemas.user as user_schema
#from starlette.requests import Request


class UserModel(Model):
    username: str
    firstName: str
    lastName: str
    hash_password: str
    permissionFor: Optional[user_schema.PermissionFor] = "- select -"
    email: EmailStr
    enrollments: Optional[List[user_schema.UserEnrollment]] = Field(default_factory=list)
    disabled: Optional[bool] = Field(default=False)
    photoUrls: Optional[List[str]] = None
    consent_given: Optional[bool] = Field(default=False)
    consent_date: Optional[int] = 0 # save in db as integer

    @property
    def formatted_consent_date(self):
        return datetime.fromtimestamp(self.consent_date).strftime('%Y-%m-%d %H:%M:%S')

    #async def __admin_repr__(self, request: Request):
        #return f"{self.lastName} {self.firstName}"

