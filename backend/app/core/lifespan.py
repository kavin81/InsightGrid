from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import RedisDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisDB.user_info.ping()
    await RedisDB.jwtr.ping()

    yield

    await RedisDB.user_info.close()
    await RedisDB.jwtr.close()
