from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.auth.jwthandler import get_current_user
from src.schemas.users import UserOutSchema
import src.repositories.download_data as download
import src.repositories.upload_data as upload
import src.repositories.update_houses as update
import src.crud.reviews as crud_reviews
import src.crud.users as crud_users
from src.schemas.reviews import ModerateReviewSchema, ReviewOutSchema


router = APIRouter()


# Проверка роли администратора
async def is_admin(user: UserOutSchema):
    user_data = await crud_users.get_user(user.username)
    if not user_data or user_data.role_name != "Admin":
        raise HTTPException(status_code=403, detail="Access denied: Admins only")
    return user_data

@router.post("/admin/download")
async def download_data(current_user: UserOutSchema = Depends(get_current_user)):
    await is_admin(current_user)
    await download.main()
    return JSONResponse(content={"message": "Download completed"})

@router.post("/admin/upload")
async def upload_data(current_user: UserOutSchema = Depends(get_current_user)):
    await is_admin(current_user)
    await upload.main()
    return JSONResponse(content={"message": "Upload completed"})

@router.post("/admin/update-houses")
async def update_houses(current_user: UserOutSchema = Depends(get_current_user)):
    await is_admin(current_user)
    await update.main()
    return JSONResponse(content={"message": "Update completed"})


@router.post("/review/moderate", response_model=ReviewOutSchema, dependencies=[Depends(get_current_user)])
async def moderate_review_route(
    data: ModerateReviewSchema,
    current_user: UserOutSchema = Depends(get_current_user)
):
    await is_admin(current_user)

    return await crud_reviews.moderate_review(
        review_id=data.review_id,
        action=data.action
    )