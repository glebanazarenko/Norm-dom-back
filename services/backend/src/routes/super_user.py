from fastapi import APIRouter, Depends, HTTPException

from src.auth.jwthandler import get_current_user
from src.schemas.reviews import EditReviewSchema, ReviewOutSchema
from src.schemas.users import UserOutSchema
from src.services.reviews import edit_review
from src.services.users import is_super_user

router = APIRouter()


@router.post("/review/edit", response_model=ReviewOutSchema, dependencies=[Depends(get_current_user)])
async def edit_review_route(
    data: EditReviewSchema,
    current_user: UserOutSchema = Depends(get_current_user)
):
    await is_super_user(current_user)
    try:
        return await edit_review(data, current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")