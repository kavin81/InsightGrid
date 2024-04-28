from fastapi import APIRouter

router = APIRouter()


@router.get("/{post_id}")
async def get_post(post_id):
    return {"post_id": f"{post_id}"}


@router.patch("/{post_id}")
async def update_post(post_id):
    return {"post_id": f"{post_id}"}


@router.delete("/{post_id}")
async def delete_post(post_id):
    return {"post_id": f"{post_id}"}
