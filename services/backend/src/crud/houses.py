from fastapi import HTTPException, Depends
from src.main import logger
from typing import List
from tortoise.expressions import Q
from src.database.models import House, Review, User
from src.schemas.houses import HouseOutSchema
from uuid import UUID
from tortoise.exceptions import IntegrityError
from src.schemas.users import UserOutSchema

async def get_house(query: str, page: int = 1, per_page: int = 10) -> List[HouseOutSchema]:
    offset = (page - 1) * per_page
    houses = await House.filter(
        Q(unom__icontains=query) |
        Q(full_address__icontains=query) |
        Q(simple_address__icontains=query)  |
        Q(full_address__icontains=query)
    ).offset(offset).limit(per_page).all()

    if houses:
        return houses
    raise HTTPException(status_code=404, detail="Нет такого дома")


async def get_house_by_id(id: UUID) -> HouseOutSchema:
    house = await House.filter(Q(id=id)).first()

    if house:
        return house

    raise HTTPException(status_code=404, detail="Нет такого дома")


async def get_or_none(id: UUID):
    return await House.get_or_none(id=id)
    

async def calculate_aggregate_rating(house_id: UUID):
    """Рейтинг дома рассчитывается только на основе опубликованных (is_published=True) и неудаленных (is_deleted=False) отзывов."""

    house = await House.get_or_none(id=house_id)
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")
    
    reviews = await Review.filter(house_id=house_id, is_published=True, is_deleted=False).all()
    total_ratings = sum(review.rating for review in reviews)
    count = len(reviews)
    
    if count == 0:
        return 0
    
    aggregate_rating = total_ratings / count
    return aggregate_rating