from uuid import UUID

from fastapi import HTTPException

from src.crud.reviews import (get_review_by_id_and_user, update_review,
                              update_review_status)
from src.schemas.reviews import (EditReviewSchema, ModerateReviewSchema,
                                 ReviewOutSchema)


async def moderate_review(data: ModerateReviewSchema) -> ReviewOutSchema:
    review = await update_review_status(
        review_id=data.review_id,
        is_published=(data.action == "approve"),
        is_deleted=(data.action == "reject")
    )

    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден")

    if data.action not in ["approve", "reject"]:
        raise HTTPException(status_code=400, detail="Недопустимое действие")

    return await review

async def edit_review(data: EditReviewSchema, user_id: UUID) -> ReviewOutSchema:
    # Получаем отзыв только если он принадлежит текущему пользователю
    review = await get_review_by_id_and_user(data.review_id, user_id)
    if not review:
        raise HTTPException(status_code=404, detail="Отзыв не найден или не принадлежит вам")
    # Обновляем данные и ставим на модерацию
    updated_review = await update_review(
        review_id=data.review_id,
        new_rating=data.new_rating,
        new_content=data.new_review_text,
        is_published=False
    )

    return updated_review