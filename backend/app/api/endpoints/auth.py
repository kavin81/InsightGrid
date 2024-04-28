# builtin
from datetime import datetime, timedelta
from typing import Any

# fastapi
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# security
from fastjwt import TokenPayload
from passlib.context import CryptContext

# app
from app.core import security, settings
from app.db.redis import RedisCrud, RedisDB, RedisModel
from app.schema import JWTToken

router = APIRouter()


@router.post("/login", response_model=JWTToken)
def login(username: str, password: str):
    # add redis support for caching

    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # extract to RedisCrud() class
    if UserData := RedisModel.UserData.find(
        (RedisModel.UserData.username == username)
        & (RedisModel.UserData.password_hash == pwd_ctx.hash(password))
    ).first():

        user_id = str(UserData.pk)

        if pwd_ctx.verify(password, UserData.password):
            access_token = security.create_access_token(uid=user_id, fresh=True)
            refresh_token = security.create_refresh_token(uid=user_id)

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.SECURITY_CONFIG.JWT_ACCESS_TOKEN_EXPIRES,
                "refresh_token": refresh_token,
            }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
    )


@router.post("/refresh")
def refresh(
    access_payload=Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")),
    refresh_payload: TokenPayload = Depends(security.refresh_token_required),
) -> dict[str, Any]:
    # if refresh_payload:
    if (access_payload.expiry_datetime + timedelta(minutes=10)) > datetime.now():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is not expired",
        )
    if RedisCrud.isRevoked(str(refresh_payload), "RT"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )
    user_id = refresh_payload.sub or ""

    access_token = security.create_access_token(uid=user_id)
    refresh_token = security.create_refresh_token(uid=user_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.SECURITY_CONFIG.JWT_ACCESS_TOKEN_EXPIRES,
        "refresh_token": refresh_token,
    }


@router.delete("/logout")
async def logout(
    access_token=Depends(OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")),
    refresh_token: TokenPayload = Depends(security.refresh_token_required),
):

    async with RedisDB.jwtr.pipeline(transaction=True) as pipeline:
        pipeline.set(
            name=f"AT_bl_{access_token}",
            value=access_token,
            ex=settings.SECURITY_CONFIG.JWT_ACCESS_TOKEN_EXPIRES,
        )
        pipeline.set(
            name=f"RT_bl_{refresh_token}",
            value=str(refresh_token),
            ex=settings.SECURITY_CONFIG.JWT_REFRESH_TOKEN_EXPIRES,
        )
        await pipeline.execute()

    return {"msg": "success"}


@router.get(
    "/whoami",
    dependencies=[Depends(security.access_token_required)],
)
async def whoami():
    return {"username": "test_user"}
