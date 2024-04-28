from app.db.redis import RedisDB, auth_r, jwtr_r


class mysql_db:
    def __init__(self, mysql_db):
        self.mysql_db = mysql_db


MySQLDB = mysql_db(...)


__all__ = ["RedisDB", "auth_r", "jwtr_r"]
