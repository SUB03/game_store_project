from fastapi import FastAPI

from app.routers import todos

api = FastAPI(title="my app")
api.include_router(todos.router)

@api.get('/')
def index():
    return {"message": "Hello world"}