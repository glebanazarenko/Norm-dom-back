from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.schemas.houses import HouseOutSchema
from uuid import UUID
from src.schemas.users import UserOutSchema
from src.schemas.houses import ReviewCreateSchema
from src.services.houses import get_searched_houses, get_house_by_id_with_logic, add_review_to_house_with_logic
from src.auth.jwthandler import get_current_user

router = APIRouter()

@router.get("/houses/search", response_model=List[HouseOutSchema])
async def search_houses(query: str):
    try:
        houses = await get_searched_houses(query)
        return houses
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/house/{id}", response_model=HouseOutSchema)
async def get_house_by_id(id: UUID):
    try:
        house = await get_house_by_id_with_logic(id)
        return house
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/house/{id}/reviews", response_model=HouseOutSchema, dependencies=[Depends(get_current_user)])
async def add_review_to_house(
    id: UUID,
    review_data: ReviewCreateSchema,  # Используем схему для валидации
    current_user: UserOutSchema = Depends(get_current_user)
):
    try:
        house = await add_review_to_house_with_logic(
            id, review_data.review_text, review_data.rating, current_user
        )
        return house
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
