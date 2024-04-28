from app.db.redis import RedisDB


def isRevoked(token: str, token_type="RT" or "AT") -> bool:
    return bool(RedisDB.jwtr.get(f"{token_type}_bl_{token}"))
