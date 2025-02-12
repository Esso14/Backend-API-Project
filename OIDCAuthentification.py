from datetime import timedelta, datetime
from typing import Optional, Annotated
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette import status

from settings import engine, SETTINGS
from models.user import UserModel


# Pydantic models for token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Blacklist to store revoked tokens
blacklist = set()

# New user
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#Function to generate and verify Tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.SECRET_KEY.get_secret_value(), algorithm=SETTINGS.ALGORITHM)
    return encoded_jwt

async def get_user_from_db(username: str) -> UserModel:
    user_data = await engine.find_one(UserModel, UserModel.username == username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

# Function to authenticate user
async def authenticate_user(username: str, password: str) -> Optional[UserModel]:
    try:
        user = await get_user_from_db(username)
        #user = await engine.find_one(UserModel, UserModel.username == username)
        if user and verify_password(password, user.hash_password):
            return user
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SETTINGS.SECRET_KEY.get_secret_value(), algorithms=[SETTINGS.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    # except InvalidTokenError:
    except JWTError:
        raise credentials_exception

    #user = await engine.find_one(UserModel, UserModel.username == token_data.username)
    user = await get_user_from_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user