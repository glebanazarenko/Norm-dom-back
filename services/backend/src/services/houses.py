from typing import List
from uuid import UUID

from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

import src.crud.reviews as crud_reviews
import src.crud.users as crud_user
from src.crud.houses import get_house, get_house_by_id, get_or_none
from src.main import logger
from src.schemas.houses import HouseOutOneSchema, HouseOutReviewSchema, HouseOutSchema
from src.schemas.users import UserOutSchema


async def add_review_to_house_with_logic(
    id: UUID, review_text: str, rating: int, current_user: UserOutSchema
) -> HouseOutReviewSchema:
    # Проверяем, существует ли дом
    house = await get_or_none(id=id)
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")

    # Получаем пользователя по id из current_user
    user = await crud_user.get(
        id=current_user.id
    )  # Заменяем current_user на экземпляр модели User
    try:
        # Создаем новый отзыв с is_published=False (на модерации)
        review = await crud_reviews.create(
            house=house, user=user, rating=rating, review_text=review_text
        )
    except IntegrityError as err:
        logger.error(f"Ошибка создания пользователя: {err}")
        raise HTTPException(status_code=400, detail=str(err))

    logger.info(f"Review data: {review}")

    # Обновляем дом с новым списком отзывов
    await house.fetch_related("reviews")  # Получаем связанные отзывы
    return await HouseOutReviewSchema.from_tortoise_orm(
        house
    )  # Возвращаем обновленный дом


async def get_searched_houses(
    query: str, page: int = 1, per_page: int = 100
) -> List[HouseOutSchema]:
    houses = await get_house(query, page, per_page)

    if not houses:
        raise HTTPException(status_code=404, detail="Нет такого дома")

    return houses


async def get_house_by_id_with_logic(house_id: UUID) -> HouseOutOneSchema:
    # Получаем дом из репозитория
    house = await get_house_by_id(house_id)

    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")

    print(f"[INFO] Получен дом с ID: {house.id}")

    return house
