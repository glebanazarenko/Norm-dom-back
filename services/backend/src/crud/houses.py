from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError
from src.main import logger
from typing import List
from tortoise.expressions import Q
from tortoise.queryset import QuerySet
from src.database.models import House
from src.schemas.houses import HouseOutSchema
from uuid import UUID




async def get_house(query: str, page: int = 1, per_page: int = 10) -> List[HouseOutSchema]:
    offset = (page - 1) * per_page
    houses = await House.filter(
        Q(unom__icontains=query) |
        Q(full_address__icontains=query) |
        Q(simple_address__icontains=query)
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

async def add_review_to_house(id: UUID, review_data: str, rating: int) -> HouseOutSchema:
    pass