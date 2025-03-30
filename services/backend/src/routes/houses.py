from fastapi import APIRouter, Depends, HTTPException
from typing import List
import src.crud.houses as crud
from src.schemas.houses import HouseOutSchema
from src.main import logger

router = APIRouter()

@router.get("/houses/search", response_model=List[HouseOutSchema])
async def search_houses(query: str):
    logger.info(f'Тест')
    if not query:
        return []
    houses = await crud.get_house(query)
    logger.info(f'Дома {houses}')
    if not houses:
        return []

    return houses