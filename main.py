# import uvicorn
from fastapi import FastAPI

# Create FastAPI application
app = FastAPI()

@app.get('/')
def index():
    return 'hello!'

@app.get('/data')
def data():
    return {'data': {'name': 'Tcha-Tokey'}}


# Start with: uvicorn main:app --reload