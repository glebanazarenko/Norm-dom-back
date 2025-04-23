from fastapi import APIRouter, Depends, HTTPException
from typing import List
import src.crud.houses as crud
from src.schemas.houses import HouseOutSchema
from src.main import logger
from uuid import UUID
from src.schemas.users import UserOutSchema
from src.schemas.houses import ReviewCreateSchema

from src.auth.jwthandler import get_current_user

router = APIRouter()

@router.get("/houses/search", response_model=List[HouseOutSchema])
async def search_houses(query: str):
    if not query:
        raise HTTPException(status_code=404, detail="Дом не найден")
    houses = await crud.get_house(query)
    logger.info(f'Дома {houses}')

    return houses


@router.get("/house/{id}", response_model=HouseOutSchema)
async def get_house_by_id(id: UUID):
    logger.info(f'Дома {id}')
    house = await crud.get_house_by_id(id)
    logger.info(f'Дома {house}')
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")
    return house


@router.post("/house/{id}/reviews", response_model=HouseOutSchema, dependencies=[Depends(get_current_user)])
async def add_review_to_house(
    id: UUID,
    review_data: ReviewCreateSchema,  # Используем схему для валидации
    current_user: UserOutSchema = Depends(get_current_user)
):
    logger.info(f"Получены данные: {review_data}")
    house = await crud.add_review_to_house(
        id, review_data.review_data, review_data.rating, current_user
    )
    logger.info(f"Дом: {house}")
    if not house:
        raise HTTPException(status_code=404, detail="Дом не найден")
    return house