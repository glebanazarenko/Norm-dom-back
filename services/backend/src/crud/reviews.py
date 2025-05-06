from uuid import UUID

from src.database.models import Review


async def create(house, user, rating: int, review_text: str):
    return await Review.create(
        house=house, user=user, rating=rating, review_text=review_text
    )


async def get_review_by_id(review_id: UUID):
    return await Review.get_or_none(id=review_id)


async def get_reviews_by_user(user):
    return await Review.filter(user=user).prefetch_related("house").all()


async def update_review_status(review_id: UUID, is_published: bool, is_deleted: bool):
    review = await Review.get_or_none(id=review_id)
    if not review:
        return None
    review.is_published = is_published
    review.is_deleted = is_deleted
    await review.save()
    return review


async def get_review_by_id_and_user(review_id: UUID, user_id: UUID):
    return await Review.get_or_none(id=review_id, user_id=user_id)


async def update_review(
    review_id: UUID, new_rating: int, new_content: str, is_published: bool = False
):
    review = await Review.get_or_none(id=review_id)
    if not review:
        return None

    review.rating = new_rating
    review.review_text = new_content
    review.is_published = is_published
    await review.save()

    return review
