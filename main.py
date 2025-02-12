from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from OIDCAuthentification import oauth2_scheme, authenticate_user, Token, create_access_token
from models.user import UserModel
from routes.user import router as user_router
from routes.course import router as course_router
from routes.task import router as task_router
from settings import SETTINGS

# Create FastAPI application
app=FastAPI()


# Add session middleware: Allow CORS (Cross-Origin Ressource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Erlaubte Ursprünge
    allow_credentials=True,   # Erlaubt Anfragen mit Authentifizierung
    allow_methods=["*"],      # Erlaubt alle HTTP-Methoden (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],      # Erlaubt alle HTTP-Header
)

# Root-Endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the demo with FastAPI!"}


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    #return Token(access_token=access_token, token_type="bearer")

app.include_router(user_router, tags=["user"])
app.include_router(course_router, tags=["course"])
app.include_router(task_router, tags=["task"])


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)


# Start with: uvicorn main:app --reload
# Info: pip install python-multipart