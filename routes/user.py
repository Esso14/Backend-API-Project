from fastapi import APIRouter, HTTPException
from models.user import UserModel
from schemas.user import NewUser, UserBaseInfos
from settings import engine
from OIDCAuthentification import get_password_hash, verify_password

router = APIRouter()

#User login
@router.get("/login", response_model=UserBaseInfos)
async def login_user(username: str, password: str):
    #hashed_password = get_password_hash(password)
    user = await engine.find_one(UserModel, UserModel.username == username)
    if user and verify_password(password, user.hash_password):
        return UserBaseInfos(
            id=str(user.id),
            username=user.username,
            firstName=user.firstName,
            lastName=user.lastName,
            permissionFor=user.permissionFor,
            email=user.email,
            disabled=user.disabled,
        )

    raise HTTPException(status_code=400, detail="Incorrect username or password")


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


#@app.post("/user", response_model=User)
#async def create_user(user: User):
#    await engine.save(user)
#    return user