from fastapi import FastAPI
from store_service.routers import store

api = FastAPI()
api.include_router(store.router)

@api.get('/')
def index():
    return {"message": "game store index"}