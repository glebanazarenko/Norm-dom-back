from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.auth.jwthandler import get_current_user
from src.schemas.houses import HouseOutSchema, ReviewCreateSchema, HouseOutOneSchema, HouseOutReviewSchema
from src.schemas.users import UserOutSchema
from src.database.models import AdmArea, District
from src.services.houses import (
    add_review_to_house_with_logic,
    get_house_by_id_with_logic,
    get_searched_houses,
)

router = APIRouter()


@router.get("/houses/search", response_model=List[HouseOutSchema])
async def search_houses(query: str):
    try:
        houses = await get_searched_houses(query)
        return houses
    except HTTPException as e:
        raise e


@router.get("/house/{id}", response_model=HouseOutOneSchema)
async def get_house_by_id(id: UUID):
    try:
        house = await get_house_by_id_with_logic(id)
        return house
    except HTTPException as e:
        raise e


@router.post(
    "/house/{id}/reviews",
    response_model=HouseOutReviewSchema,
    dependencies=[Depends(get_current_user)],
)
async def add_review_to_house(
    id: UUID,
    review_data: ReviewCreateSchema,  # Используем схему для валидации
    current_user: UserOutSchema = Depends(get_current_user),
):
    try:
        house = await add_review_to_house_with_logic(
            id, review_data.review_text, review_data.rating, current_user
        )
        return house
    except HTTPException as e:
        raise e
    

@router.get("/houses/unique-adm-areas")
async def get_unique_adm_areas():
    # Query to get unique adm_areas
    adm_areas = await AdmArea.all()
    return {"adm_areas": adm_areas}

@router.get("/houses/unique-districts")
async def get_unique_districts():
    # Query to get unique districts
    districts = await District.all()
    return {"districts": districts}
