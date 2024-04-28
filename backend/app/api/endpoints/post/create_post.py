from fastapi import APIRouter

router = APIRouter()


@router.get("/{user_id}")
async def get_users(user_id):
    return {"username": f"{user_id}"}
