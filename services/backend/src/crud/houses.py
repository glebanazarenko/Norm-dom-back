from fastapi import HTTPException
from src.main import logger
from typing import List
from tortoise.expressions import Q
from src.database.models import House, Review, User
from src.schemas.houses import HouseOutSchema
from uuid import UUID
from src.schemas.users import UserOutSchema
from src.auth.jwthandler import get_current_user
from fastapi import Depends




async def get_house(query: str, page: int = 1, per_page: int = 10) -> List[HouseOutSchema]:
    offset = (page - 1) * per_page
    houses = await House.filter(
        Q(unom__icontains=query) |
        Q(full_address__icontains=query) |
        Q(simple_address__icontains=query)  |
        Q(full_address__icontains=query)
    ).offset(offset).limit(per_page).all()

    if houses:
        # Используем HouseOutSchema для сериализации данных
        return [await HouseOutSchema.from_tortoise_orm(house) for house in houses]
    raise HTTPException(status_code=404, detail="Нет такого дома")


async def get_house_by_id(id: UUID) -> HouseOutSchema:
    house = await House.filter(Q(id=id)).first()

    if house:
        # Используем HouseOutSchema для сериализации данных
        return await HouseOutSchema.from_tortoise_orm(house)

    raise HTTPException(status_code=404, detail="Нет такого дома")

async def add_review_to_house(id: UUID, review_data: str, rating: int, current_user: UserOutSchema) -> HouseOutSchema:
    # Проверяем, существует ли дом
    house = await House.get_or_none(id=id)
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")
    
    # Получаем пользователя по id из current_user
    user = await User.get(id=current_user.id)  # Заменяем current_user на экземпляр модели User
    
    # Создаем новый отзыв
    await Review.create(
        house=house,
        user=user,
        rating=rating,
        review_text=review_data
    )
    
    # Обновляем дом с новым списком отзывов
    await house.fetch_related("reviews")  # Получаем связанные отзывы
    return await HouseOutSchema.from_tortoise_orm(house)  # Возвращаем обновленный дом