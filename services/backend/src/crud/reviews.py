from fastapi import HTTPException, Depends
from src.main import logger
from src.database.models import Review
from uuid import UUID
from src.schemas.users import UserOutSchema


async def edit_review(review_id: UUID, new_rating: int, new_review_text: str, current_user: UserOutSchema):
    review = await Review.get_or_none(id=review_id, user_id=current_user.id)
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден или не принадлежит вам")
    
    # Отправляем отзыв на повторную модерацию
    review.rating = new_rating
    review.review_text = new_review_text
    review.is_published = False  # На модерации
    
    await review.save()
    return review


async def moderate_review(review_id: UUID, action: str):
    review = await Review.get_or_none(id=review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")
    
    if action == "approve":
        review.is_published = True
        review.is_deleted = False
    elif action == "reject":
        review.is_published = False
        review.is_deleted = True
    else:
        raise HTTPException(status_code=400, detail="Недопустимое действие")
    
    await review.save()
    return review

async def create(house, user, rating: int, review_data: str):
    return await Review.create(
        house=house,
        user=user,
        rating=rating,
        review_text=review_data
    )