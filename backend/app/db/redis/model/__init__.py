from app.db.redis.model.user import UserData


class redis_model:
    def __init__(self):
        self.UserData = UserData


RedisModel = redis_model()
