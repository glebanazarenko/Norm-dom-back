from fastapi import HTTPException, Depends
from src.main import logger
from src.schemas.houses import HouseOutSchema
from uuid import UUID
from tortoise.exceptions import IntegrityError
from src.schemas.users import UserOutSchema
import src.crud.houses as crud_house
import src.crud.users as crud_user
import src.crud.reviews as crud_reviews


async def add_review_to_house(id: UUID, review_data: str, rating: int, current_user: UserOutSchema) -> HouseOutSchema:
    # Проверяем, существует ли дом
    house = await crud_house.get_or_none(id=id)
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")
    
    # Получаем пользователя по id из current_user
    user = await crud_user.get(id=current_user.id)  # Заменяем current_user на экземпляр модели User
    try:
        # Создаем новый отзыв с is_published=False (на модерации)
        review = await crud_reviews.create(
            house=house,
            user=user,
            rating=rating,
            review_text=review_data
        )
    except IntegrityError as err:
        logger.error(f"Ошибка создания пользователя: {err}")
        raise HTTPException(status_code=400, detail=str(err))

    logger.info(f'Review data: {review}')
    
    # Обновляем дом с новым списком отзывов
    await house.fetch_related("reviews")  # Получаем связанные отзывы
    return await HouseOutSchema.from_tortoise_orm(house)  # Возвращаем обновленный дом