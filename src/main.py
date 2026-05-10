from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.db import db_manager


@asynccontextmanager
async def lifespan(_app: FastAPI):

    yield
    await db_manager.engine.dispose()


app = FastAPI(lifespan=lifespan)
