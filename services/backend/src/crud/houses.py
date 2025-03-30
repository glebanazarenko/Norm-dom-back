from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError
from src.main import logger
from typing import List
from tortoise.expressions import Q
from tortoise.queryset import QuerySet
from src.database.models import House
from src.schemas.houses import HouseOutSchema




async def get_house(query: str, page: int = 1, per_page: int = 10) -> List[HouseOutSchema]:
    logger.info(f'Начало поиска дома {query}')
    offset = (page - 1) * per_page
    houses = await House.filter(
        Q(unom__icontains=query) |
        Q(full_address__icontains=query) |
        Q(simple_address__icontains=query)
    ).offset(offset).limit(per_page).all()

    logger.info(f'House data: {houses}')

    if houses:
        # Используем HouseOutSchema для сериализации данных
        return [await HouseOutSchema.from_tortoise_orm(house) for house in houses]
    raise HTTPException(status_code=400, detail="Нет такого дома")
