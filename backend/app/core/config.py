from datetime import timedelta
from functools import lru_cache

from fastjwt import FJWTConfig
from pydantic_settings import BaseSettings


# Note: .env file values override => default values declared here)
class Settings(BaseSettings):

    # FastAPI Config
    PROJECT_NAME: str = "FastAPI"
    PROJECT_DESCRIPTION: str = "A FastAPI project."
    API_VER: str = "/"
    VERSION: str = "0.1.0"
    # FastAPI docs
    OPENAPI_URL: str = "/openapi.json"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    # FastJWT Config
    SECURITY_CONFIG: FJWTConfig = FJWTConfig(
        # ---- dev ----
        JWT_ALGORITHM="HS256",
        JWT_SECRET_KEY="NwMp9IDQXu3bfqUth+xhcQdCxHEgXzZ/SU5guFhDeH0=",
        # --- prod ---
        JWT_TOKEN_LOCATION=["headers"],
        JWT_HEADER_NAME="Authorization",
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(hours=4),
    )
    # Redis connection
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "password"
    REDIS_SSL: bool = True

    # .env file config
    class Config:
        env_file = (
            ".env"  # Note: .env file values override => default values declared here)
        )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

__all__ = ["settings"]
