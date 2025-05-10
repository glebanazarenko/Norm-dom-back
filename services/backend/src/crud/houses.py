import re
from typing import List
from uuid import UUID

import tortoise
from fastapi import HTTPException
from tortoise.expressions import Q
from tortoise.functions import Avg

from src.database.models import House, Review
from src.schemas.houses import HouseOutOneSchema, HouseOutSchema


async def get_house(
    query: str, page: int = 1, per_page: int = 10
) -> List[HouseOutSchema]:
    print(f"[DEBUG] Получен запрос: {query}")

    offset = (page - 1) * per_page
    houses = (
        await House.filter(
            Q(unom__icontains=query)
            | Q(full_address__icontains=query)
            | Q(simple_address__icontains=query)
            | Q(full_address__icontains=query)
        )
        .prefetch_related("adm_area", "district", "photos", "reviews")
        .offset(offset)
        .limit(per_page)
        .all()
    )

    if not houses:
        raise HTTPException(status_code=404, detail="Нет такого дома")

    # Создаём список выходных схем с учётом avg_rating
    result = []
    for house in houses:
        published_reviews = await Review.filter(house=house, is_published=True).all()
        avg_rating = "0"
        total = "0"
        if published_reviews:
            total = sum(review.rating for review in published_reviews)
            avg_rating = total / len(published_reviews)
            avg_rating = str(round(avg_rating, 1))

        # Теперь photos и reviews уже загружены через prefetch_related
        data = {
            "id": house.id,
            "unom": house.unom,
            "full_address": house.full_address,
            "simple_address": house.simple_address,
            "created_at": house.created_at,
            "updated_at": house.updated_at,
            "reviews": [str(review.id) for review in house.reviews],
            "adm_area": house.adm_area.name if house.adm_area else None,
            "district": house.district.name if house.district else None,
            "rating": avg_rating,
            "rating_count": str(len(published_reviews)),
        }
        result.append(HouseOutSchema(**data))

    return result


async def get_house_by_id(house_id: UUID) -> HouseOutOneSchema:
    # Получаем дом по ID и аннотируем средним рейтингом
    house = await (
        House.filter(id=house_id)
        .prefetch_related("adm_area", "district", "photos", "reviews")
        .first()
    )

    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")

    published_reviews = await Review.filter(house=house, is_published=True).all()
    avg_rating = "0"
    total = "0"
    if published_reviews:
        total = sum(review.rating for review in published_reviews)
        avg_rating = total / len(published_reviews)
        avg_rating = str(round(avg_rating, 1))

    match = re.match(r"POINT \(([\d\.-]+)\s([\d\.-]+)\)", house.geodata_center)
    if not match:
        longitude, latitude = None, None
    longitude, latitude = map(float, match.groups())

    data = {
        "id": house.id,
        "unom": house.unom,
        "full_address": house.full_address,
        "simple_address": house.simple_address,
        "created_at": house.created_at,
        "updated_at": house.updated_at,
        "kad_n": house.kad_n,
        "kad_zu": house.kad_zu,
        "geo_data": house.geo_data,
        "geodata_center": house.geodata_center,
        "latitude": latitude,
        "longitude": longitude,
        "photos": [str(photo.id) for photo in house.photos],
        "reviews": list(house.reviews),
        "adm_area": house.adm_area.name if house.adm_area else None,
        "district": house.district.name if house.district else None,
        "rating": avg_rating,
        "rating_count": str(len(published_reviews)),
    }

    return HouseOutOneSchema(**data)


async def get_or_none(id: UUID):
    return await House.get_or_none(id=id)


async def calculate_aggregate_rating(house_id: UUID):
    """Рейтинг дома рассчитывается только на основе опубликованных (is_published=True) и неудаленных (is_deleted=False) отзывов."""

    house = await House.get_or_none(id=house_id)
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")

    reviews = await Review.filter(
        house_id=house_id, is_published=True, is_deleted=False
    ).all()
    total_ratings = sum(review.rating for review in reviews)
    count = len(reviews)

    if count == 0:
        return 0

    aggregate_rating = total_ratings / count
    return aggregate_rating
