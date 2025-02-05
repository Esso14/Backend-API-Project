from datetime import timedelta, datetime
from typing import Optional
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBasic
from pydantic import BaseModel
from passlib.context import CryptContext
from starlette import status

from settings import engine, SETTINGS
from models.user import UserModel

security = HTTPBasic()

# Pydantic models for token
class Token(BaseModel):
    access_token: str
    token_type: str

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Blacklist to store revoked tokens
blacklist = set()

# New user
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_from_db(username: str):
    user_data = await engine.find_one(UserModel, username == username)
    if not user_data:
        raise HTTPException(status_code=400, detail="User not found")
    return user_data


def authenticate_user(username: str, password: str):
    user = get_user_from_db(username)
    if not user:
        return False
    hashed_password = user["hash_password"]
    if not verify_password(password, hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.SECRET_KEY, algorithm=SETTINGS.ALGORITHM)
    return encoded_jwt


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=[SETTINGS.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = await get_user_from_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
