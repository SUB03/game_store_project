from fastapi import FastAPI

from app.engine import lifespan
from app.routers import todos, users

api = FastAPI(title="my app", lifespan=lifespan)
api.include_router(todos.router)
api.include_router(users.router)

@api.get('/')
def index():
    return {"message": "Hello world"}