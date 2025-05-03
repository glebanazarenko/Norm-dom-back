from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

import src.utils.download_data as download
import src.utils.update_houses as update
import src.utils.upload_data as upload
from src.auth.jwthandler import get_current_user
from src.schemas.reviews import ModerateReviewSchema, ReviewOutSchema
from src.schemas.users import UserOutSchema
from src.services.reviews import moderate_review
from src.services.users import is_admin

router = APIRouter()


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


@router.post("/review/moderate", response_model=ReviewOutSchema)
async def moderate_review_route(
    data: ModerateReviewSchema, current_user: UserOutSchema = Depends(get_current_user)
):
    await is_admin(current_user)
    try:
        return await moderate_review(data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
