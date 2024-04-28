from redis.asyncio import Redis

from app.core import settings

redis_config = {
    "host": settings.REDIS_HOST,
    "port": settings.REDIS_PORT,
    "password": settings.REDIS_PASSWORD,
    "ssl": settings.REDIS_SSL,
}

user_info_r: Redis = Redis(
    **redis_config,
    db=0,
)


jwtr_r: Redis = Redis(
    **redis_config,
    db=1,
)


class redis_db:

    async def __init__(self, auth: Redis = user_info_r, jwtr: Redis = jwtr_r):
        self.user_info: Redis = await auth
        self.jwtr: Redis = await jwtr


RedisDB = redis_db(auth=user_info_r, jwtr=jwtr_r)

__all__ = ["RedisDB"]
