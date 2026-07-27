from fastapi import FastAPI

from auth_service.engine import lifespan
from auth_service.routers import users

api = FastAPI(title="my app", lifespan=lifespan)
api.include_router(users.router)

@api.get('/')
def index():
    return {"message": "Hello world"}

#TODO: schedule token table cleanup