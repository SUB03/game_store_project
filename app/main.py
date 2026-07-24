from fastapi import FastAPI

from app.routers import todos, users

api = FastAPI(title="my app")
api.include_router(todos.router)
api.include_router(users.router)

@api.get('/')
def index():
    return {"message": "Hello world"}