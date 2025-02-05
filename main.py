import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import router as user_router
from routes.course import router as course_router
from routes.task import router as task_router

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

app.include_router(user_router, tags=["user"])
app.include_router(course_router, tags=["course"])
app.include_router(task_router, tags=["task"])


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)


# Start with: uvicorn main:app --reload