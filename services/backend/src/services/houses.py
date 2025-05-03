from fastapi import HTTPException, Depends
from src.main import logger
from typing import List
from src.schemas.houses import HouseOutSchema
from uuid import UUID
from tortoise.exceptions import IntegrityError
from src.schemas.users import UserOutSchema
from src.crud.houses import get_or_none, get_house, get_house_by_id
import src.crud.users as crud_user
import src.crud.reviews as crud_reviews


async def add_review_to_house_with_logic(id: UUID, review_text: str, rating: int, current_user: UserOutSchema) -> HouseOutSchema:
    # Проверяем, существует ли дом
    house = await get_or_none(id=id)
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
            review_text=review_text
        )
    except IntegrityError as err:
        logger.error(f"Ошибка создания пользователя: {err}")
        raise HTTPException(status_code=400, detail=str(err))

    logger.info(f'Review data: {review}')
    
    # Обновляем дом с новым списком отзывов
    await house.fetch_related("reviews")  # Получаем связанные отзывы
    return await HouseOutSchema.from_tortoise_orm(house)  # Возвращаем обновленный дом


async def get_searched_houses(query: str, page: int = 1, per_page: int = 10) -> List[HouseOutSchema]:
    if not query:
        raise HTTPException(status_code=400, detail="Пустой запрос")

    houses = await get_house(query, page, per_page)

    if not houses:
        raise HTTPException(status_code=404, detail="Нет такого дома")
    
    logger.info(f'Дома {houses}')

    # Используем HouseOutSchema для сериализации данных
    return [await HouseOutSchema.from_tortoise_orm(house) for house in houses]

async def get_house_by_id_with_logic(house_id: UUID) -> HouseOutSchema:

    # Получаем дом из репозитория
    house = await get_house_by_id(house_id)
    
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")
    
    # Дополнительная бизнес-логика
    # Например: логируем запрос
    print(f"[INFO] Получен дом с ID: {house.id}")

    # Можно добавить проверки, права доступа, кэширование и т.д.

    # Сериализуем модель в Pydantic
    return await HouseOutSchema.from_tortoise_orm(house)