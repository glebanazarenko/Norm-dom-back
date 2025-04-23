from fastapi import APIRouter, Depends, HTTPException
from src.auth.jwthandler import get_current_user
from src.schemas.users import UserOutSchema
import src.crud.reviews as crud_reviews
import src.crud.users as crud_users
from src.schemas.reviews import EditReviewSchema, ReviewOutSchema


router = APIRouter()

# Проверка роли суперпользователя
async def is_super_user(user: UserOutSchema):
    user_data = await crud_users.get_user(user.username)
    if not user_data or user_data.role_name != "Super User":
        raise HTTPException(status_code=403, detail="Access denied: Super Users only")
    return user_data


@router.post("/review/edit", response_model=ReviewOutSchema, dependencies=[Depends(get_current_user)])
async def edit_review_route(
    data: EditReviewSchema,
    current_user: UserOutSchema = Depends(get_current_user)
):
    await is_super_user(current_user)
    # Вызываем бизнес-логику для редактирования отзыва
    result = await crud_reviews.edit_review(
        review_id=data.review_id,
        new_rating=data.new_rating,
        new_review_text=data.new_review_text,
        current_user=current_user
    )
    return result
