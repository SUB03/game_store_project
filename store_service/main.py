from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from store_service.routers import store

api = FastAPI()
api.include_router(store.router)

# origins = [
#     "localhost:"
# ]

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get('/')
def index():
    return {"message": "game store index"}