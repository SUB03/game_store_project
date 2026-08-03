from contextlib import asynccontextmanager

from fastapi import FastAPI
import yaml, atexit
import logging
import logging.config
import logging.handlers

from auth_service.engine import engine
from auth_service.routers import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("auth_service has started")
    yield
    logger.info("auth_service has stopped")
    await engine.dispose()

def setup_logging():
    with open("auth_service/logger_config.yml") as f:
        config = yaml.safe_load(f)
    logging.config.dictConfig(config)
    queue_handler: logging.handlers.QueueHandler | None = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


logger = logging.getLogger("auth_service")

api = FastAPI(title="my app", lifespan=lifespan)
api.include_router(users.router)

@api.get('/')
def index():
    logger.info("visited root")
    return {"message": "Hello world"}

#TODO: schedule token table cleanup