from fastjwt import FastJWT

from app.core.config import settings

security = FastJWT(config=settings.SECURITY_CONFIG)

__all__ = ["security"]
