from fastapi import APIRouter

from app.api.endpoints import auth_router, user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/user", tags=["users", "user-info"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication", "login"])
