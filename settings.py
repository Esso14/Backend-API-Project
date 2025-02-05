from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from pydantic import Field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    # Secret key to encode the JWT token
    # to get a string like this run: openssl rand -hex 32
    SECRET_KEY: SecretStr = Field(
        "a7faafeb786ce4ce7fe10b60ab262441e9958d281122bd69578d54a9ead56109"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

SETTINGS = _Settings()

# Verbindung zur MongoDB herstellen
MONGO_DETAILS = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DETAILS)
engine = AIOEngine(client, database="MyTutorium_DB")
#engine = AIOEngine(database="MyTutorium_DB", uri=MONGO_DETAILS)
