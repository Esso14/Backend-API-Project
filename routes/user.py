from fastapi import APIRouter, HTTPException
from models.user import UserModel
from schemas.user import NewUser
from settings import engine
from OIDCAuthentification import get_password_hash

router = APIRouter()

#User login
@router.get("/login", response_model=UserModel)
async def login_user(username: str, password: str):
    user = await engine.find_one(UserModel, username=username, passwort=get_password_hash(password))
    if user:
        return user
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