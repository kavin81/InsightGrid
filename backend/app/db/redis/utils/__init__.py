from app.db.redis.utils.is_revoked import isRevoked


class redis_crud:
    def __init__(self):
        self.isRevoked = isRevoked


RedisCrud = redis_crud()


__all__ = ["RedisCrud"]
