from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from models.user import UserModel
from schemas.user import NewUser, UserBaseInfos
from settings import engine
from OIDCAuthentification import get_password_hash, verify_password, get_current_user, get_current_active_user

router = APIRouter()

# Get me
@router.get("/user/me/", response_model=UserBaseInfos)
#@router.get("/user/me/", response_model=UserModel)
async def get_me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    #return current_user
    return UserBaseInfos(
        id=str(current_user.id),
        username=current_user.username,
        firstName=current_user.firstName,
        lastName=current_user.lastName,
        permissionFor=current_user.permissionFor,
        email=current_user.email,
        disabled=current_user.disabled,
    )

@router.post("/user/new/", response_model=UserModel)
async def create_user(user: NewUser):
    user_instanz = UserModel(
        username=user.username,
        firstName=user.firstName,
        lastName=user.lastName,
        hash_password=get_password_hash(user.password),
        email=user.email,
        photoUrls=user.photoUrls,
    )
    await engine.save(user_instanz)
    return user_instanz


