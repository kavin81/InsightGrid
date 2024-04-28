from datetime import timedelta

from pydantic import BaseModel, Field


class JWTToken(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer")
    expires_in: timedelta = Field(
        default=timedelta(minutes=15), description="Token expiration time"
    )
    refresh_token: str = Field(..., description="JWT refresh token")
